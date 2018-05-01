import tensorflow as tf
sess = tf.InteractiveSession()

raw = tf.constant([-1, 0, 1])

onehot = tf.one_hot(raw, depth=3, axis=-1)

# Add print operation
ptr = tf.Print(onehot, [onehot], message="This is a: ")

ptr.eval()