import functools
import tensorflow as tf


def doublewrap(function):
    @functools.wraps(function)
    def decorator(*args, **kwargs):
        if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
            return function(args[0])
        else:
            return lambda wrapee: function(wrapee, *args, **kwargs)
    return decorator


@doublewrap
def define_scope(function, scope=None, *args, **kwargs):
    attribute = '_cache_' + function.__name__
    name = scope or function.__name__
    @property
    @functools.wraps(function)
    def decorator(self):
        if not hasattr(self, attribute):
            with tf.variable_scope(name, *args, **kwargs):
                setattr(self, attribute, function(self))
        return getattr(self, attribute)
    return decorator


class Model:

    def __init__(self, n_days, n_dyn_feature, n_sta_feature, n_out, init_lr, base_layers, fusion_layers):
        self.init_lr = init_lr
        self.n_days = n_days
        self.base_layers = base_layers
        self.fusion_layers = fusion_layers
        self.n_out = n_out
        self.n_sta_feature = n_sta_feature

        self.data_rnn = tf.placeholder(tf.float32, [None, n_days, n_dyn_feature], name='dynamic_feature')
        self.data_nn = tf.placeholder(tf.float32, [None, n_sta_feature], name='static_feature')
        self.label = tf.placeholder(tf.float32, [None, n_out], name='label')

        self.step = tf.Variable(0, trainable=False)
        self.learning_rate = tf.train.exponential_decay(self.init_lr, self.step, 5000, 0.9)
        self.keep_prob = tf.placeholder(tf.float32)

        self.lstm
        self.dnn
        self.fusion
        self.prediction
        self.loss
        self.optimize

        tf.summary.scalar("loss", self.loss)
        tf.summary.scalar("learning_rate", self.learning_rate)
        self.merged = tf.summary.merge_all()

    @define_scope
    def lstm(self):
        cells = []
        for k in self.base_layers:
            cells.append(tf.contrib.rnn.LayerNormBasicLSTMCell(k, activation=tf.nn.elu,
                                                               dropout_keep_prob=self.keep_prob))
        m_cell = tf.contrib.rnn.MultiRNNCell(cells, state_is_tuple=True)
        init_state = m_cell.zero_state(tf.shape(self.data_nn)[0], dtype=tf.float32)
        val, _ = tf.nn.dynamic_rnn(m_cell, inputs=self.data_rnn, initial_state=init_state, time_major=False)
        val = tf.transpose(val, [1, 0, 2])
        return tf.gather(val, self.n_days - 1)

    @define_scope(initializer=tf.contrib.layers.xavier_initializer())
    def dnn(self):
        dnn_out = self.data_nn
        if self.n_sta_feature > 1:
            for k in self.base_layers:
                dnn_out = tf.contrib.layers.fully_connected(dnn_out, k, activation_fn=tf.nn.elu)
        return dnn_out

    @define_scope
    def fusion(self):
        fusion_out = tf.concat([self.dnn, self.lstm], axis=-1)
        for k in self.fusion_layers:
            fusion_out = tf.contrib.layers.fully_connected(fusion_out, k, activation_fn=tf.nn.tanh)
        return fusion_out

    @define_scope(initializer=tf.contrib.layers.xavier_initializer())
    def prediction(self):
        return tf.contrib.layers.fully_connected(self.fusion, self.n_out, activation_fn=tf.nn.tanh)

    @define_scope
    def loss(self):
        return tf.reduce_mean(tf.square(self.prediction - self.label))

    @define_scope
    def optimize(self):
        optimizer = tf.train.GradientDescentOptimizer(self.learning_rate)
        return optimizer.minimize(self.loss, global_step=self.step)

    @define_scope
    def eval(self):
        return tf.reduce_mean(tf.abs(self.prediction - self.label))