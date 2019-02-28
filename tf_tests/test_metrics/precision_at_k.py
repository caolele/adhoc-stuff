# Refer to https://stackoverflow.com/questions/45603956/class-wise-precision-and-recall-for-multi-class-classification-in-tensorflow

import tensorflow as tf

labels = tf.constant([[2],[0]],tf.int64)
# labels = tf.constant([[0,0,1,0],[1,0,0,0]],tf.int64)
predictions = tf.constant([[0.5,0.3,0.1,0.1],[0.5,0.3,0.1,0.1]])

metric = tf.metrics.precision_at_k(labels, predictions, 1, class_id=2)

sess = tf.Session()
sess.run(tf.local_variables_initializer())

precision, update = sess.run(metric)
print(precision) # 0.5