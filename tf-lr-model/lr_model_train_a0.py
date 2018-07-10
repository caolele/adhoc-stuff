import os, sys
import random
import tensorflow as tf
import pandas as pd
from model_wrapper import define_scope
# from tensorflow.python.saved_model import builder as saved_model_builder
# from tensorflow.python.saved_model import tag_constants

tf.app.flags.DEFINE_integer('dispf', 50, 'display_frequency.')
tf.app.flags.DEFINE_integer('epoch', 100, 'number of epochs.')
tf.app.flags.DEFINE_integer('ver', 1, 'version number of the model.')
tf.app.flags.DEFINE_integer('bs', 2048, 'batch size of training.')
tf.app.flags.DEFINE_float('lr', 0.1, 'initial learning rate.')
tf.app.flags.DEFINE_integer('lrds', 1000, 'lr_exp_decay: decay_steps.')
tf.app.flags.DEFINE_float('lrdr', 0.5, 'lr_exp_decay: decay_rate.')
tf.app.flags.DEFINE_string('dir', './model', 'Working directory.')
FLAGS = tf.app.flags.FLAGS


class Model:

    def __init__(self, init_lr=0.01, ds=1000, dr=0.8):
        # placeholders for input data
        self.feature1 = tf.placeholder(tf.float32, (None, 1), name='feature1')
        self.feature2 = tf.placeholder(tf.float32, (None, 1), name='feature2')
        self.feature3 = tf.placeholder(tf.float32, (None, 1), name='feature3')

        self.data_crossover
        self.label = tf.placeholder(tf.float32, (None, 1), name='label')

        # initialize weight (uniform) and bias (zeros)
        # self.W = tf.Variable([[0.014622], [0.75116], [-0.02281]], name='weights')
        # self.b = tf.Variable([[-0.00774]], name='bias')
        self.W = tf.Variable(tf.random_uniform([3, 1]), name='weights')  # need to sync weights initialization method
        self.b = tf.Variable(tf.random_uniform([1]), name='bias')

        self.step = tf.Variable(0, trainable=False)
        self.learning_rate = tf.train.exponential_decay(init_lr, self.step, ds, dr)

        self.basic_lr
        self.loss
        self.optimize

    # apply crossover between the two raw features
    @define_scope
    def data_crossover(self):
        # feature12 = self.feature1 * self.feature2
        return tf.concat([self.feature1, self.feature2, self.feature3], -1)

    # linear model  y = X*W + b
    @define_scope
    def basic_lr(self):
        return tf.add(tf.matmul(self.data_crossover, self.W), self.b,  name='predict_op')

    @define_scope
    def loss(self):
        return tf.losses.mean_squared_error(labels=self.label, predictions=self.basic_lr)

    @define_scope
    def optimize(self):
        optimizer = tf.train.AdamOptimizer(self.learning_rate)
        return optimizer.minimize(self.loss, global_step=self.step)


def load_csv_data(file):
    if file[-4:] != ".csv":
        file += ".csv"
    if os.path.isfile(file):
        raw_data = pd.read_csv(file)
        hc_spend = raw_data["c2"]
        hc_spend_x_case_num = raw_data["c12"]
        raw_data["c2"] = (hc_spend - hc_spend.mean()) / hc_spend.std()
        raw_data["c12"] = (hc_spend_x_case_num - hc_spend_x_case_num.mean()) / hc_spend_x_case_num.std()
        label_hc_spend = raw_data["l1"]
        raw_data["l1"] = (label_hc_spend - label_hc_spend.mean()) / label_hc_spend.std()
        return raw_data[["iid"]], \
               raw_data[["c1", "c2", "c12"]], \
               raw_data[["l1"]]
    else:
        print("Error: Data file " + file + "not found!")
        exit(1)


def main(_):
    print('Epoch:%d | Version:%d | BatchSize:%d | LeaningRateDecay:%f,%d,%f | Directory:%s'
          % (FLAGS.epoch, FLAGS.ver, FLAGS.bs, FLAGS.lr, FLAGS.lrds, FLAGS.lrdr, FLAGS.dir))

    export_path = os.path.join(FLAGS.dir, str(FLAGS.ver))

    ids, features, labels = load_csv_data("data_sample")
    x = features.values
    y = labels.values
    n_train = ids.shape[0]
    print('Data Loaded. ID shape:'+str(ids.shape)
          + ', Feature shape:'+str(features.shape)
          + ', Label shape:'+str(labels.shape))

    # initialize model
    model = Model(init_lr=FLAGS.lr, ds=FLAGS.lrds, dr=FLAGS.lrdr)
    saver = tf.train.Saver()
    init_op = tf.global_variables_initializer()
    sess = tf.InteractiveSession()
    sess.run(init_op)
    print('Model initialized.')

    # training
    n_batches = int(n_train / FLAGS.bs)
    disp_freq = FLAGS.dispf
    for i in range(FLAGS.epoch):
        aidx = list(range(n_train))
        random.shuffle(aidx)

        ptr, loss = 0, 0
        print('Training: initLr = %f, batchSize = %d' % (FLAGS.lr, FLAGS.bs))
        sys.stdout.flush()
        _j = 1
        for j in range(n_batches):
            chunk_x1 = x[aidx[ptr:ptr + FLAGS.bs], :1]
            chunk_x2 = x[aidx[ptr:ptr + FLAGS.bs], 1:2]
            chunk_x3 = x[aidx[ptr:ptr + FLAGS.bs], 2:]
            chunk_y = y[aidx[ptr:ptr + FLAGS.bs], :]
            ptr += FLAGS.bs

            _, _ce, _lr = sess.run([model.optimize, model.loss, model.learning_rate],
                                   feed_dict={model.feature1: chunk_x1,
                                              model.feature2: chunk_x2,
                                              model.feature3: chunk_x3,
                                              model.label: chunk_y})
            loss += _ce

            if (j + 1) % disp_freq == 0 or j + 1 == n_batches:
                print('Epoch %d/%d Batch %d/%d: loss = %f , lr = %f'
                      % (i + 1, FLAGS.epoch, j + 1, n_batches, loss / _j, _lr))
                sys.stdout.flush()
                loss = 0
                _j = 1
            else:
                _j += 1

    '''
    print('Exporting trained model to', export_path)
    builder = saved_model_builder.SavedModelBuilder(export_path)
    builder.add_meta_graph_and_variables(sess, [tag_constants.SERVING])
    builder.save(True)
    '''

    print('Saving trained model to', export_path)
    saver.save(sess, export_path)


    sess.close()


if __name__ == '__main__':
    tf.app.run()