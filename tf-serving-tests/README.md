docker pull tensorflow/serving:1.6.1-devel

docker run -it -p 4001:4001 --name tensorflow_serving -v ~/adhoc-stuff/tf-serving-tests/dvol:/dvol tensorflow/serving:1.6.1-devel

nohup tensorflow_model_server --enable_batching=true --batching_parameters_file=/tensorflow-serving/model_config/batching_conf.txt --port=4001 --model_config_file=/tensorflow-serving/model_config/mlp_20180725.conf > serving.log 2>&1 &


/fjord/sites/tensorflow/models