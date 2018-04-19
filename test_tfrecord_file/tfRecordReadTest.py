import tensorflow as tf
import numpy as np


def simple_read_test(filename):

    for serialized_example in tf.python_io.tf_record_iterator(filename):
        example = tf.train.Example()
        example.ParseFromString(serialized_example)
        ''' an example of getting array data
        idata = example.features.feature['active_history_30days'].float_list.value
        idata = np.reshape(np.array(idata), (15, 33))
        '''
        kpid = example.features.feature['kpid'].int64_list.value
        country = example.features.feature['country'].bytes_list.value
        

def read_and_decode(filename):

    filename_queue = tf.train.string_input_producer([filename])
    reader = tf.TFRecordReader()
    _, serialized_example = reader.read(filename_queue)
    features = tf.parse_single_example(serialized_example,
                                       features={
                                           'kpid': tf.FixedLenFeature([], tf.int64),
                                           'country' : tf.FixedLenFeature([], tf.string),
                                       })

    # d = tf.decode_raw(features['idata'], tf.float32)
    # d = tf.reshape(features['idata'], [15, 33])
    # l = tf.cast(features['label'], tf.int32)

    return features['kpid'], features['country']


f1, f2 = read_and_decode("simplereader_out-00000-of-00004")

f1_batch, f2_batch = tf.train.shuffle_batch([f1, f2],
                                            batch_size=5,
                                            capacity=5000,
                                            min_after_dequeue=2000,
                                            allow_smaller_final_batch=True)

init = tf.initialize_all_variables()

with tf.Session() as sess:
    sess.run(init)
    threads = tf.train.start_queue_runners(sess=sess)

    with open('decoded_output.txt', 'wb') as outfile:
        for i in range(100):
            val1, val2 = sess.run([f1_batch, f2_batch])
            for j in range(5):
                print("LALALALA", val1[j])
                np.savetxt(outfile, [val1[j]], fmt="kpid:%d", delimiter=",")
                np.savetxt(outfile, [val2[j]], fmt="country:%s", delimiter=",")
                outfile.write(str.encode("\n"))

sess.close()
