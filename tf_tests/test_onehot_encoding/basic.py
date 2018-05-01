import tensorflow as tf

raw1 = tf.Variable([0, 1, 2])
raw2 = tf.Variable([-1, 0, 1]) + tf.Variable([1], dtype=tf.int32)

onehot = tf.one_hot(raw2, depth=3, axis=-1)

argmax = tf.argmax(onehot, -1)

init_op = tf.initialize_all_variables()

#run the graph
with tf.Session() as sess:
    sess.run(init_op) #execute init_op
    #print the random values that we sample

    print (sess.run(onehot))

    print (sess.run(argmax))