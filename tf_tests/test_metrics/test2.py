import tensorflow as tf
import kingml
import numpy as np
from sklearn.metrics import roc_auc_score, accuracy_score, precision_score, recall_score, f1_score
from kingml.metrics.f1_score import metric_f1_score

y_true_1d = [1, 1, 0, 0, 0, 1, 0, 1]
y_pred_1d = [0, 1, 0, 0, 1, 1, 1, 1]

y_true_2d = [[0,1], [0,1], [1,0], [1,0], [1,0], [0,1], [1,0], [0,1]]
y_pred_2d = [[1,0], [0,1], [1,0], [1,0], [0,1], [0,1], [0,1], [0,1]]

y_pred_1d_prob = tf.constant([0.25,0.56,0.43,0.4,0.77,0.89,0.9,0.65])
y_pred_1d_prob_np = [0.25,0.56,0.43,0.4,0.77,0.89,0.9,0.65]

accuracy_1d = tf.metrics.accuracy(
    y_true_1d, y_pred_1d
)

accuracy_2d = tf.metrics.accuracy(
    y_true_2d, y_pred_2d
)

precision_1d = tf.metrics.precision(
    y_true_1d, y_pred_1d
)

precision_2d = tf.metrics.precision(
    y_true_2d, y_pred_2d
)

recall_1d = tf.metrics.recall(
    y_true_1d, y_pred_1d
)

recall_2d = tf.metrics.recall(
    y_true_2d, y_pred_2d
)

f1_1d = metric_f1_score(
    y_true_1d, y_pred_1d
)

f1_2d = metric_f1_score(
    y_true_2d, y_pred_2d
)

auc_1d = tf.metrics.auc(
	y_true_1d, y_pred_1d_prob
)

with tf.Session() as sess:
    sess.run(tf.local_variables_initializer())
    print('accuracy_tf_1d: {}'.format(sess.run(accuracy_1d)[1]))
    print('accuracy_tf_2d: {}'.format(sess.run(accuracy_2d)[1]))
    print('accuracy_skl_1d: {}'.format(accuracy_score(y_true_1d, y_pred_1d)))
    # print('accuracy_skl_2d: {}'.format(accuracy_score(y_true_2d, y_pred_2d)))

    print()

    print('precision_tf_1d: {}'.format(sess.run(precision_1d)[1]))
    print('precision_tf_2d: {}'.format(sess.run(precision_2d)[1]))
    print('precision_skl_1d: {}'.format(precision_score(y_true_1d, y_pred_1d)))

    print()

    print('recall_tf_1d: {}'.format(sess.run(recall_1d)[1]))
    print('recall_tf_2d: {}'.format(sess.run(recall_2d)[1]))
    print('recall_skl_1d: {}'.format(recall_score(y_true_1d, y_pred_1d)))

    print()

    print('f1_tf_1d: {}'.format(sess.run(f1_1d)[1]))
    print('f1_tf_2d: {}'.format(sess.run(f1_2d)[1]))
    print('f1_skl_1d: {}'.format(f1_score(y_true_1d, y_pred_1d)))

    print()

    print('auc_tf_1d: {}'.format(sess.run(auc_1d)[1]))
    print('auc_skl_1d: {}'.format(roc_auc_score(y_true_1d, y_pred_1d_prob_np)))


