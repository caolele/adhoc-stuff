import tensorflow as tf
import numpy as np


x = tf.placeholder(tf.float32,[3,3])
y = tf.placeholder(tf.float32,[4,3])


w0 = tf.Variable(tf.ones([3,3]))

w1 = tf.Variable(tf.ones([4,3]))

w2 = tf.Variable(tf.ones([3,3]))

mult_x_w0 = tf.matmul(x,w0)  # op1

mult_w1_op1 = tf.stop_gradient(tf.matmul(w1,mult_x_w0))  # op2

mult_w2_w0 = tf.matmul(w2, w0)  # op4
mult_w2_w0 = tf.stop_gradient(mult_w2_w0)

mult_op2_w2 = tf.matmul(mult_w1_op1, w2)  # op3

output = tf.matmul(mult_op2_w2, mult_w2_w0)  # op5

loss = output - y
optimizer = tf.train.GradientDescentOptimizer(1).minimize(loss)


with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    print("*****before gradient descent*****")
    print("w0---\n",w0.eval(),"\n","w1---\n",w1.eval(),"\n","w2---\n",w2.eval())
    w0_,w1_,w2_,_ = sess.run([w0,w1,w2,optimizer],feed_dict = {x:np.random.normal(size = (3,3)),y:np.random.normal(size = (4,3))})
    print("*****after gradient descent*****")
    print("w0---\n",w0_,"\n","w1---\n",w1_,"\n","w2---\n",w2_)
