import tensorflow as tf
import pandas as pd
import os

from src.utilities.data_io import get_one_batch
from src.utilities.pre_proc import pre_process_data, pre_process_label
from src.model.lstm_model import Model
from src.utilities.cai_logger import get_logger

from tensorflow.python.saved_model import builder as saved_model_builder
from tensorflow.python.saved_model import signature_constants
from tensorflow.python.saved_model import signature_def_utils
from tensorflow.python.saved_model import tag_constants
from tensorflow.python.saved_model import utils

tf.app.flags.DEFINE_integer('ver', 1, 'version number of the model.')
tf.app.flags.DEFINE_integer('bs', 16, 'batch size of training.')
tf.app.flags.DEFINE_float('lr', 0.0005, 'initial learning rate.')
tf.app.flags.DEFINE_float('num_iter', 100000, 'the total number of iterations to be trained.')
tf.app.flags.DEFINE_float('num_day', 10, 'the number of days in a time-series.')
tf.app.flags.DEFINE_string('dir', '../dump', 'Working directory.')
FLAGS = tf.app.flags.FLAGS


def main(_):

    log = get_logger();

    data, data_mean, data_std = pre_process_data()
    label, label_mean, label_std = pre_process_label()
    # print(data.shape)
    # print(label.shape)
    nan_rows = data[pd.isnull(data).any(axis=1)]
    if not nan_rows.empty:
        print(nan_rows)
        raise ValueError("Error: The input data missing values!")

    model = Model(FLAGS.num_day, data.shape[-1] + 2, 1, label.shape[-1], FLAGS.lr, [512, 128, 16], [128, 32])

    # define model signature
    tensor_info_x_dyn = utils.build_tensor_info(model.data_rnn)
    tensor_info_x_sta = utils.build_tensor_info(model.data_nn)
    tensor_info_y = utils.build_tensor_info(model.prediction)
    reg_signature = signature_def_utils.build_signature_def(
        inputs={'x_dyn': tensor_info_x_dyn,
                'x_sta': tensor_info_x_sta},
        outputs={'scores': tensor_info_y},
        method_name=signature_constants.REGRESS_METHOD_NAME
    )

    # init graph etc.
    init_op = tf.global_variables_initializer()
    sess = tf.InteractiveSession()
    sess.run(init_op)
    saver = tf.train.Saver()
    file_writer = tf.summary.FileWriter(FLAGS.dir, sess.graph)


    # one fp+bp
    for itr in range(FLAGS.num_iter):

        batch_data, batch_case, batch_label = get_one_batch(data, label, FLAGS.bs, FLAGS.num_day)

        _, _ce1, _lr, summary = sess.run([model.optimize, model.loss, model.learning_rate, model.merged],
                                feed_dict={model.data_rnn: batch_data,
                                           model.data_nn: batch_case,
                                           model.label: batch_label,
                                           model.keep_prob: 0.9})

        log.info("Iteration step {}; loss={}; lr={}".format(itr, _ce1, _lr))

        # scalars
        file_writer.add_summary(summary, itr)

        if itr % (FLAGS.num_iter / 10) == 0 and itr > 0:
            save_path = saver.save(sess, os.path.join(FLAGS.dir, "snapshot_" + str(itr) + ".ckpt"))
            log.info("Model snapshot is saved at {}".format(save_path))
            '''
            meta_path = os.path.join(FLAGS.dir, "model.meta")
            meta_graph_def = tf.train.export_meta_graph(filename=meta_path)
            print("Model meta graph is stored at {}".format(meta_path))
            '''



    # exp model for tfserving
    export_path = os.path.join(FLAGS.dir, str(FLAGS.ver))
    log.info('Exporting trained model to', export_path)
    builder = saved_model_builder.SavedModelBuilder(export_path)
    builder.add_meta_graph_and_variables(sess, [tag_constants.SERVING],
                                         signature_def_map={
                                             signature_constants.DEFAULT_SERVING_SIGNATURE_DEF_KEY: reg_signature})
    builder.save(True)

    sess.close()



if __name__ == '__main__':
    tf.app.run()
