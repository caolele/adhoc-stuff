import sys
import tensorflow as tf
from grpc.beta import implementations
import numpy as np
import predict_pb2
import prediction_service_pb2

tf.app.flags.DEFINE_string("host", "127.0.0.1", "gRPC server host")
tf.app.flags.DEFINE_integer("port", 4001, "gRPC server port")
tf.app.flags.DEFINE_string("model_name", "lele1", "TensorFlow model name")
tf.app.flags.DEFINE_integer("model_ver", 1532506656, "TensorFlow model version")
tf.app.flags.DEFINE_float("req_timeout", 10.0, "Timeout of gRPC request")
FLAGS = tf.app.flags.FLAGS

def trans4user(rs):
    res = []
    for j in range(0, rs.shape[0]):
            tmp = rs[j, 2:]
            res.append(tmp)
    return np.array([res])

def main(_):

    data_mock = np.random.rand(2,11)
    print("data_mock =", data_mock)

    dyn_tensor_str = tf.contrib.util.make_tensor_proto(data_mock, dtype=tf.float32, shape=data_mock.shape).SerializeToString()
    dyn_tensor_str_proto = tf.contrib.util.make_tensor_proto(dyn_tensor_str, dtype=tf.string, shape=[2])
    print("data_serialized =", dyn_tensor_str_proto)
    
    # Create gRPC client and request
    print('Processing inference proto ...')
    channel = implementations.insecure_channel(FLAGS.host, FLAGS.port)
    stub = prediction_service_pb2.beta_create_PredictionService_stub(channel)
    request = predict_pb2.PredictRequest()
    request.model_spec.name = FLAGS.model_name
    request.model_spec.version.value = FLAGS.model_ver
    request.model_spec.signature_name = 'serving_default'
    request.inputs['examples'].CopyFrom(dyn_tensor_str_proto)

    # Send request
    print('Inferencing ...')
    rsp = stub.Predict(request, FLAGS.req_timeout)
    print(rsp)


if __name__ == '__main__':
  tf.app.run()