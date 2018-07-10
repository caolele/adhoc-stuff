import tensorflow as tf

tf.app.flags.DEFINE_string('meta', './model/1.meta', 'Location of meta file')
tf.app.flags.DEFINE_string('chkpts', './model/', 'Location of checkpoints file')
FLAGS = tf.app.flags.FLAGS


def main(_):
    sess = tf.Session()
    saver = tf.train.import_meta_graph(FLAGS.meta)
    saver.restore(sess, tf.train.latest_checkpoint(FLAGS.chkpts))

    graph = tf.get_default_graph()
    fea1 = graph.get_tensor_by_name("feature1:0")
    fea2 = graph.get_tensor_by_name("feature2:0")
    fea3 = graph.get_tensor_by_name("feature3:0")
    feed_dict = {fea1: [[0.0], [1.0]], fea2: [[17.0], [17.0]], fea3: [[0.0], [17.0]]}

    weights = graph.get_tensor_by_name("weights:0")
    bias = graph.get_tensor_by_name("bias:0")
    print(sess.run([weights, bias]))

    basic_lr = graph.get_tensor_by_name("basic_lr/predict_op:0")
    print(sess.run(basic_lr, feed_dict))


if __name__ == '__main__':
    tf.app.run()