# A Basic operation using tensorflow
import tensorflow as tf

# Define 2 tensorflow constants
a = tf.constant(2, name="a")
b = tf.constant(3, name="b")
# Use the tensorflow function 'add' to add the two constants
c = tf.add(a, b, name="c")
# Tensorflow now creates a graph and runs it in a session.
sess = tf.Session()
result = sess.run(c)
print(result)
# Close the session
sess.close()
