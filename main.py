from features import Features
from embedding import Glove
from utils import GloveDataSet, GeneralDataSet
import tensorflow as tf
import numpy as np


glove = Glove()
# glove.parse('data/glove.840B.300d.txt')
# glove.dump('data/glove.840B.300d')

chars = set()
glove.load('data/glove.840B.300d')


data = GloveDataSet(glove, Features())
data.dump('data/dataset')

data = GeneralDataSet()
data.load('data/dataset')

_x, _y = data.all_data()

x = tf.placeholder(tf.float32, (_x.shape[1], None))
y = tf.placeholder(tf.float32, (_y.shape[1], None))

w1 = tf.get_variable('w1', (1000, _x.shape[1]), initializer=tf.random_normal_initializer(mean=0.0, stddev=0.1))
b1 = tf.get_variable('b1', (1000, 1), initializer=tf.random_normal_initializer())
w2 = tf.get_variable('w2', (800, 1000), initializer=tf.random_normal_initializer(mean=0.0, stddev=0.01))
b2 = tf.get_variable('b2', (800, 1), initializer=tf.random_normal_initializer())
w3 = tf.get_variable('w3', (600, 800), initializer=tf.random_normal_initializer(mean=0.0, stddev=0.01))
b3 = tf.get_variable('b3', (600, 1), initializer=tf.random_normal_initializer())
w4 = tf.get_variable('w4', (400, 600), initializer=tf.random_normal_initializer(mean=0.0, stddev=0.01))
b4 = tf.get_variable('b4', (400, 1), initializer=tf.random_normal_initializer())
w5 = tf.get_variable('w5', (_y.shape[1], 400), initializer=tf.random_normal_initializer(mean=0.0, stddev=0.00001))
b5 = tf.get_variable('b5', (_y.shape[1], 1), initializer=tf.random_normal_initializer())

w0 = tf.get_variable('w0', (_y.shape[1], 1000), initializer=tf.random_normal_initializer(mean=0.0, stddev=0.000001))
b0 = tf.get_variable('b0', (_y.shape[1], 1), initializer=tf.random_normal_initializer())


z1 = tf.add(tf.matmul(w1, x), b1)
a1 = tf.nn.tanh(z1)

z0 = tf.add(tf.matmul(w0, z1), b0)
a5 = tf.nn.tanh(z0)

'''
z2 = tf.add(tf.matmul(w2, z1), b2)
a2 = tf.nn.tanh(z2)

z3 = tf.add(tf.matmul(w3, z2), b3)
a3 = tf.nn.tanh(z3)

z4 = tf.add(tf.matmul(w4, z3), b4)
a4 = tf.nn.tanh(z4)

z5 = tf.add(tf.matmul(w5, z4), b5)
a5 = tf.nn.tanh(z5)

'''

cost = tf.reduce_mean(tf.pow(a5 - y, 2))

optimizer = tf.train.AdamOptimizer(learning_rate=0.001).minimize(cost)

init_op = tf.global_variables_initializer()

with tf.Session() as sess:
    sess.run(init_op)

    for i in range(100):
        _, c = sess.run([optimizer, cost], feed_dict={x: np.transpose(_x), y: np.transpose(_y)})
        print(c)


