# -*- coding: utf-8 -*-
# @Time : 2021/5/12 19:38

import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
import tensorflow as tf
import numpy as np
tf.compat.v1.set_random_seed(1)

GAMMA = 0.8
A_LR = 0.0003
C_LR = 0.0009
BATCH = 32
A_UPDATE_STEPS = 10
UPDATE_STEPS = 10
S_DIM = 4
A_DIM = 7
epsilon = 0.2

class MASAC (object):
    def __init__(self):
        self.tfs = tf.placeholder(tf.float32, [None, S_DIM], 'state')
        config = tf.ConfigProto(device_count={"CPU":1},
                                inter_op_parallelism_threads=1,
                                intra_op_parallelism_threads=8,
                                log_device_placement=True)
        self.sess = tf.Session(config=config)
        # self.sess = tf.Session()
        # critic
        l1 = tf.layers.dense(self.tfs, 200, tf.nn.relu, kernel_initializer=tf.random_normal_initializer(0., .1))
        self.v = tf.layers.dense(l1, 1)
        self.tfdc_r = tf.placeholder(tf.float32, [None, 1], name='discounted_r')
        self.advantage = self.tfdc_r - self.v
        closs = tf.reduce_mean(tf.square(self.advantage))
        self.ctrain = tf.train.AdamOptimizer(C_LR).minimize(closs)

        # actor
        self.pi, pi_params = self._build_anet('pi', trainable=True)
        oldpi, oldpi_params = self._build_anet('oldpi', trainable=False)
        self.update_oldpi_op = [oldp.assign(p) for p, oldp in zip(pi_params, oldpi_params)]

        # loss
        self.tfa = tf.placeholder(tf.int32, [None, ], 'action')
        self.tfadv = tf.placeholder(tf.float32, [None, 1], 'advantage')
        a_indices = tf.stack([tf.range(tf.shape(self.tfa)[0], dtype=tf.int32), self.tfa], axis=1)
        pi_prob = tf.gather_nd(params=self.pi, indices=a_indices)   # shape=(None, )
        oldpi_prob = tf.gather_nd(params=oldpi, indices=a_indices)  # shape=(None, )
        ratio = tf.divide(pi_prob, oldpi_prob + 1e-5)
        surr = ratio * self.tfadv                       # surrogate loss
        self.aloss = -tf.reduce_mean(tf.minimum(
            surr,
            tf.clip_by_value(ratio, 1. - epsilon, 1. + epsilon)*self.tfadv))

        # actor train
        self.atrain_op = tf.train.AdamOptimizer(A_LR).minimize(self.aloss)

        self.saver = tf.train.Saver()
        # tf.summary.FileWriter("log/", self.sess.graph)
        self.sess.run(tf.global_variables_initializer())

    def update(self, data):
        self.sess.run(self.update_oldpi_op)
        data = np.vstack(data)
        s, a, r = data[:, :S_DIM], data[:, S_DIM: S_DIM + 1].ravel(), data[:, -1:]
        adv = self.sess.run(self.advantage, {self.tfs: s, self.tfdc_r: r})
        [self.sess.run(self.atrain_op, {self.tfs: s, self.tfa: a, self.tfadv: adv}) for _ in range(UPDATE_STEPS)]
        [self.sess.run(self.ctrain, {self.tfs: s, self.tfdc_r: r}) for _ in range(UPDATE_STEPS)]

    def _build_anet(self, name, trainable):
        with tf.variable_scope(name):
            l_a = tf.layers.dense(self.tfs, 200, tf.nn.relu, kernel_initializer=tf.random_normal_initializer(0., .1),
                                  trainable=trainable)
            l_b = tf.layers.dense(l_a, 100, tf.nn.relu, kernel_initializer=tf.random_normal_initializer(0., .1),
                                  trainable=trainable)
            a_prob = tf.layers.dense(l_b, A_DIM, tf.nn.softmax, trainable=trainable)
        params = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope=name)
        return a_prob, params

    def choose_action(self, s):
        prob_weights = self.sess.run(self.pi, feed_dict={self.tfs: s[None, :]})
        action = np.random.choice(range(prob_weights.shape[1]),
                                      p = prob_weights.ravel())  # select action w.r.t the actions prob
        return action

    def choose_action_max(self, s):
        prob_weights = self.sess.run(self.pi, feed_dict={self.tfs: s[None, :]})
        return np.argmax(prob_weights)

    def get_v(self, s):
        if s.ndim < 2:
            s = s[np.newaxis, :]
        return self.sess.run(self.v, {self.tfs: s})[0, 0]

    def save_model(self, path, step):
        self.saver.save(self.sess, path, global_step=step)

    def load_model(self, path):
        self.saver.restore(self.sess, path)

