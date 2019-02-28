import tensorflow as tf
import kingml
import numpy as np
from sklearn.metrics import roc_auc_score

y_true = [1, 1, 0, 0, 0, 1]
y_pred = [0, 1, 0, 0, 1, 1]

y_true_tf = [[0,1], [0,1], [1,0], [1,0], [1,0], [0,1]]
y_pred_ = [[1,0], [0,1], [1,0], [1,0], [0,1], [0,1]]
y_pred_prob_auc = tf.constant([[0.2,0.8],[0.1,0.9],[0.4,0.6],[0.6,0.4],[0.7,0.3],[0.8,0.2]])

y_true = [1, 1, 0, 0, 0, 1]
y_pred_prob = [0.8,0.77,0.6,0.4,0.3,0.5]
y_pred_prob_tf = tf.constant([0.8,0.77,0.6,0.4,0.3,0.5])


accuracy = tf.metrics.accuracy(
    y_true_tf, y_pred_
)

precision = tf.metrics.precision(
    y_true_tf, y_pred_
)

recall = tf.metrics.recall(
    y_true_tf, y_pred_
)

auc = tf.metrics.auc(
	y_true_tf, y_pred_prob_auc
)

# Run the update op and get the updated value
with tf.Session() as sess:
    sess.run(tf.local_variables_initializer())
    print('accuracy: expect {}, got {}'.format(4/6, sess.run(accuracy)[1]))
    print('precision: expect {}, got {}'.format(2/3, sess.run(precision)[1]))
    print('recall: expect {}, got {}'.format(2/3, sess.run(recall)[1]))
    print('AUC: expect {}, got {}'.format('not known', sess.run(auc)))
    print("sklearn auc: {}".format(roc_auc_score(y_true, y_pred_prob)))