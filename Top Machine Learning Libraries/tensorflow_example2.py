# A Hello World code using Tensorflow
import tensorflow as tf

hello = tf.constant("Hello, TensorFlow!")
# Start tf session
sess = tf.Session()
# Run the op
print(sess.run(hello))
