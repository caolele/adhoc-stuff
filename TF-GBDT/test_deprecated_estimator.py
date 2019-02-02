#!/usr/bin/env python

import argparse
import os
import sys

import copy

import numpy as np
import tensorflow as tf

from tensorflow.contrib.boosted_trees.proto import learner_pb2
from tensorflow.contrib.layers.python.layers import feature_column
from tensorflow.contrib.learn import learn_runner

from tensorflow.contrib.boosted_trees.python.utils import losses
from tensorflow.contrib.learn.python.learn.estimators import estimator
from tensorflow.contrib.learn.python.learn.estimators import head as head_lib
from tensorflow.python.ops import math_ops

from tensorflow.contrib.boosted_trees.estimator_batch import estimator_utils
from tensorflow.contrib.boosted_trees.estimator_batch import trainer_hooks
from tensorflow.contrib.boosted_trees.python.ops import model_ops
from tensorflow.contrib.boosted_trees.python.training.functions import gbdt_batch
from tensorflow.python.framework import ops
from tensorflow.python.ops import state_ops
from tensorflow.python.training import training_util

FLAGS = None


class GradientBoostedDecisionTreeClassifier(estimator.Estimator):

    def __init__(self,
                 learner_config,
                 examples_per_layer,
                 n_classes=2,
                 num_trees=None,
                 feature_columns=None,
                 weight_column_name=None,
                 model_dir=None,
                 config=None,
                 label_keys=None,
                 feature_engineering_fn=None,
                 logits_modifier_function=None,
                 center_bias=True,
                 use_core_libs=False,
                 output_leaf_index=False):

        if n_classes > 2:
            # For multi-class classification, use our loss implementation that
            # supports second order derivative.
            def loss_fn(labels, logits, weights=None):
                result = losses.per_example_maxent_loss(
                    labels=labels,
                    logits=logits,
                    weights=weights,
                    num_classes=n_classes)
                return math_ops.reduce_mean(result[0])
        else:
            loss_fn = None
        head = head_lib.multi_class_head(
            n_classes=n_classes,
            weight_column_name=weight_column_name,
            enable_centered_bias=False,
            loss_fn=loss_fn,
            label_keys=label_keys)
        if learner_config.num_classes == 0:
            learner_config.num_classes = n_classes
        elif learner_config.num_classes != n_classes:
            raise ValueError("n_classes (%d) doesn't match learner_config (%d)." %
                             (learner_config.num_classes, n_classes))
        super(GradientBoostedDecisionTreeClassifier, self).__init__(
            model_fn=model_fn,
            params={
                'head': head,
                'feature_columns': feature_columns,
                'learner_config': learner_config,
                'num_trees': num_trees,
                'weight_column_name': weight_column_name,
                'examples_per_layer': examples_per_layer,
                'center_bias': center_bias,
                'logits_modifier_function': logits_modifier_function,
                'use_core_libs': use_core_libs,
                'output_leaf_index': output_leaf_index
            },
            model_dir=model_dir,
            config=config,
            feature_engineering_fn=feature_engineering_fn)


def model_fn(features, labels, mode, params, config):
    head = params["head"]
    learner_config = params["learner_config"]
    examples_per_layer = params["examples_per_layer"]
    feature_columns = params["feature_columns"]
    weight_column_name = params["weight_column_name"]
    num_trees = params["num_trees"]
    use_core_libs = params["use_core_libs"]
    logits_modifier_function = params["logits_modifier_function"]
    output_leaf_index = params["output_leaf_index"]

    if features is None:
        raise ValueError("At least one feature must be specified.")

    if config is None:
        raise ValueError("Missing estimator RunConfig.")

    center_bias = params["center_bias"]

    if isinstance(features, ops.Tensor):
        features = {features.name: features}

    # Make a shallow copy of features to ensure downstream usage
    # is unaffected by modifications in the model function.
    training_features = copy.copy(features)
    training_features.pop(weight_column_name, None)
    global_step = training_util.get_global_step()
    with ops.device(global_step.device):
        ensemble_handle = model_ops.tree_ensemble_variable(
            stamp_token=0,
            tree_ensemble_config="",  # Initialize an empty ensemble.
            name="ensemble_model")

    # Create GBDT model.
    gbdt_model = gbdt_batch.GradientBoostedDecisionTreeModel(
        is_chief=config.is_chief,
        num_ps_replicas=config.num_ps_replicas,
        ensemble_handle=ensemble_handle,
        center_bias=center_bias,
        examples_per_layer=examples_per_layer,
        learner_config=learner_config,
        feature_columns=feature_columns,
        logits_dimension=head.logits_dimension,
        features=training_features,
        use_core_columns=use_core_libs,
        output_leaf_index=output_leaf_index)
    with ops.name_scope("gbdt", "gbdt_optimizer"):
        predictions_dict = gbdt_model.predict(mode)
        logits = predictions_dict["predictions"]
        if logits_modifier_function:
            logits = logits_modifier_function(logits, features, mode)

        def _train_op_fn(loss):
            """Returns the op to optimize the loss."""
            update_op = gbdt_model.train(loss, predictions_dict, labels)
            with ops.control_dependencies(
                    [update_op]), (ops.colocate_with(global_step)):
                update_op = state_ops.assign_add(global_step, 1).op
                return update_op

    create_estimator_spec_op = getattr(head, "create_estimator_spec", None)

    training_hooks = []
    if num_trees:
        if center_bias:
            num_trees += 1

        finalized_trees, attempted_trees = gbdt_model.get_number_of_trees_tensor()
        training_hooks.append(
            trainer_hooks.StopAfterNTrees(num_trees, attempted_trees,
                                          finalized_trees))

    if use_core_libs and callable(create_estimator_spec_op):
        model_fn_ops = head.create_estimator_spec(
            features=features,
            mode=mode,
            labels=labels,
            train_op_fn=_train_op_fn,
            logits=logits)
        model_fn_ops = estimator_utils.estimator_spec_to_model_fn_ops(
            model_fn_ops)
    else:
        model_fn_ops = head.create_model_fn_ops(
            features=features,
            mode=mode,
            labels=labels,
            train_op_fn=_train_op_fn,
            logits=logits)

    if output_leaf_index and gbdt_batch.LEAF_INDEX in predictions_dict:
        model_fn_ops.predictions[gbdt_batch.LEAF_INDEX] = predictions_dict[
            gbdt_batch.LEAF_INDEX]

    model_fn_ops.training_hooks.extend(training_hooks)
    return model_fn_ops


def _get_tfbt(output_dir, feature_cols):
    """Configures TF Boosted Trees estimator based on flags."""
    learner_config = learner_pb2.LearnerConfig()

    learner_config.learning_rate_tuner.fixed.learning_rate = FLAGS.learning_rate
    learner_config.regularization.l1 = 0.0
    # Set the regularization per instance in such a way that
    # regularization for the full training data is equal to l2 flag.
    learner_config.regularization.l2 = FLAGS.l2 / FLAGS.batch_size
    learner_config.constraints.max_tree_depth = FLAGS.depth
    learner_config.growing_mode = learner_pb2.LearnerConfig.LAYER_BY_LAYER

    run_config = tf.contrib.learn.RunConfig(save_checkpoints_secs=30, model_dir=output_dir)

    # Create a TF Boosted trees regression estimator.
    estimator = GradientBoostedDecisionTreeClassifier(
        learner_config=learner_config,
        examples_per_layer=FLAGS.examples_per_layer,
        n_classes=2,
        num_trees=FLAGS.num_trees,
        feature_columns=feature_cols,
        config=run_config,
        center_bias=False
    )

    return estimator


def _matrix_to_dict(matrix, col_names):
    return {
        feat_name: matrix[:, feat_idx, np.newaxis]
        for feat_idx, feat_name in enumerate(col_names)}


def _make_input_fn(which_set):
    data = np.load('airlines_data.npz')
    feature_names = data['feature_names']

    feature_columns = [feature_column.real_valued_column(
        k) for k in feature_names]

    if which_set == 'train':
        return feature_columns, tf.estimator.inputs.numpy_input_fn(
            x=_matrix_to_dict(data['X_train'], feature_names),
            y=data['y_train'],
            batch_size=32,
            num_epochs=None,
            shuffle=True)
    elif which_set == 'test':
        return feature_columns, tf.estimator.inputs.numpy_input_fn(
            x=_matrix_to_dict(data['X_test'], feature_names),
            y=data['y_test'],
            num_epochs=1,
            shuffle=False)
    else:
        raise NotImplementedError()


def _make_experiment_fn(output_dir):
    feature_columns, train_input_fn = _make_input_fn('train')
    feature_columns, test_input_fn = _make_input_fn('test')

    return tf.contrib.learn.Experiment(
        estimator=_get_tfbt(output_dir, feature_columns),
        train_input_fn=train_input_fn,
        eval_input_fn=test_input_fn,
        train_steps=None,
        eval_metrics=None,
        eval_steps=None,  # Run through the test data once
    )


def main(unused_argv):
    learn_runner.run(
        experiment_fn=_make_experiment_fn,
        output_dir=FLAGS.output_dir,
        schedule='train_and_evaluate')

    # Run inference on the test dataset
    feature_columns, test_input_fn = _make_input_fn('test')

    estimator = _get_tfbt(FLAGS.output_dir, feature_columns)
    results = estimator.predict(input_fn=test_input_fn)

    y_predict = np.array([r['probabilities'][1] for r in results])
    np.save(os.path.join(FLAGS.output_dir, 'pred_tf.npy'), y_predict)


if __name__ == '__main__':
    tf.logging.set_verbosity(tf.logging.INFO)
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--batch_size",
        type=int,
        default=10000,
        help="The batch size for reading data.")
    parser.add_argument(
        "--depth",
        type=int,
        default=6,
        help="Maximum depth of weak learners.")
    parser.add_argument(
        "--l2",
        type=float,
        default=1.0,
        help="l2 regularization per batch.")
    parser.add_argument(
        "--learning_rate",
        type=float,
        default=0.1,
        help="Learning rate (shrinkage weight) with which each new tree is added.")
    parser.add_argument(
        "--examples_per_layer",
        type=int,
        default=5000,
        help="Number of examples to accumulate stats for per layer.")
    parser.add_argument(
        "--num_trees",
        type=int,
        default=10,
        help="Number of trees to grow before stopping.")

    FLAGS, unparsed = parser.parse_known_args()

    FLAGS.output_dir = 'outputs/tf_t{:03d}_d{:02d}_ex{:05d}'.format(
        FLAGS.num_trees, FLAGS.depth, FLAGS.examples_per_layer)

    tf.app.run(main=main, argv=[sys.argv[0]] + unparsed)
