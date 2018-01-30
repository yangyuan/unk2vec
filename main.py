from features import Features
from embedding import Glove
from utils import GloveDataSet, GeneralDataSet
import utils
import tensorflow as tf
import numpy as np


glove = Glove()
# glove.parse('data/glove.840B.300d.txt')
# glove.dump('data/glove.840B.300d')

# glove.load('data/glove.840B.300d')
# data = GloveDataSet(glove, Features())
# data.dump('data/dataset')

data = GeneralDataSet()
data.load('data/dataset')

_x, _y = data.all_train_data()
_x_t, _y_t = data.test_data()

x = tf.placeholder(tf.float32, (None, _x.shape[1]))
y = tf.placeholder(tf.float32, (None, _y.shape[1]))


layer_1 = tf.contrib.layers.fully_connected(
    inputs=x,
    num_outputs=1200,
    activation_fn=tf.nn.tanh)

layer_2 = tf.contrib.layers.fully_connected(
    inputs=layer_1,
    num_outputs=600,
    activation_fn=tf.nn.tanh)

_out = tf.contrib.layers.fully_connected(
    inputs=layer_2,
    num_outputs=_y.shape[1],
    activation_fn=tf.nn.tanh)

cost = tf.reduce_mean(tf.pow(_out - y, 2))

optimizer = tf.train.AdamOptimizer().minimize(cost)

init_op = tf.global_variables_initializer()


with tf.Session() as sess:
    sess.run(init_op)

    for i in range(100):
        for batch_x, batch_y in utils.batches(_x, _y, 1000):
            _, c = sess.run([optimizer, cost], feed_dict={x: batch_x, y: batch_y})
            print(c)
        c = sess.run(cost, feed_dict={x: _x_t, y: _y_t})
        print('test: ', c)


