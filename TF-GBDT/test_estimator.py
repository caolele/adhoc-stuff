#!/usr/bin/env python

import argparse
import os
import sys

import copy

import numpy as np
import tensorflow as tf

from tensorflow.contrib.learn import learn_runner

FLAGS = None


def _get_tfbt(output_dir, feature_cols):

    run_config = tf.contrib.learn.RunConfig(save_checkpoints_secs=30, model_dir=output_dir)

    # Create a TF Boosted trees regression estimator.
    return tf.estimator.BoostedTreesClassifier(
        n_batches_per_layer=int(FLAGS.examples_per_layer / FLAGS.batch_size),
        n_classes=2,
        n_trees=FLAGS.num_trees,
        max_depth=FLAGS.depth,
        learning_rate=FLAGS.learning_rate,
        l1_regularization=0.0,
        l2_regularization=FLAGS.l2 / FLAGS.batch_size,
        feature_columns=feature_cols,
        config=run_config,
        center_bias=False
    )


def _matrix_to_dict(matrix, col_names):
    return {
        feat_name: matrix[:, feat_idx, np.newaxis]
        for feat_idx, feat_name in enumerate(col_names)}


def _make_input_fn(which_set):
    data = np.load('airlines_data.npz')
    feature_names = data['feature_names']

    feature_columns = [tf.feature_column.bucketized_column(tf.feature_column.numeric_column(k), [1, 2, 3, 4, 5, 6, 10, 20, 100]) for k in feature_names]

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
