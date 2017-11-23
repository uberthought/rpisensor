import tensorflow as tf
import numpy as np
import os.path
import math

def sigmoid(v):
    if v < -700:
        return 0
    else:
        return (1.0 / (1.0 + math.exp(-v)) - 0.5) * 2.0

class DQN:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size

        self.stddev = tf.placeholder_with_default(0.0, [])

        self.state_input = tf.placeholder(tf.float32, shape=(None, state_size))
        noise_vector = tf.random_normal(shape=tf.shape(self.state_input), mean=0.0, stddev=self.stddev, dtype=tf.float32)
        noise = tf.add(self.state_input, noise_vector)

        units = 8
        hidden1 = tf.layers.dense(inputs=noise, units=units, activation=tf.nn.relu)
        hidden2 = tf.layers.dense(inputs=hidden1, units=units, activation=tf.nn.relu)
        # hidden3 = tf.layers.dense(inputs=hidden2, units=units, activation=tf.nn.relu)
        self.prediction = tf.layers.dense(inputs=hidden2, units=self.action_size)
        self.expected = tf.placeholder(tf.float32, shape=(None, self.action_size))
        self.loss = tf.reduce_mean(tf.losses.mean_squared_error(self.expected, self.prediction))
        self.run_train = tf.train.AdagradOptimizer(.1).minimize(self.loss)

        self.sess = tf.Session()
        self.sess.run(tf.global_variables_initializer())

        if os.path.exists('train/graph.meta'):
                print("loading training data")
                saver = tf.train.Saver()
                saver.restore(self.sess, 'train/graph')

    def run(self, states):
        return self.sess.run(self.prediction, feed_dict={self.state_input: states})

    def save(self):
        saver = tf.train.Saver()
        saver.save(self.sess, 'train/graph')

    def train(self, experiences):
        X = np.array([], dtype=np.float).reshape(0, self.state_input.shape[1])
        Y = np.array([], dtype=np.float).reshape(0, self.action_size)

        if (len(experiences.get()) > 1000):
            training_experiences = np.random.choice(experiences.get(), 1000)
        else:
            training_experiences = experiences.get()

        # training_experiences = experiences.get()

        for experience in training_experiences:
            actions0 = self.run([experience.state0])
            actions1 = self.run([experience.state1])
            discount_factor = .1
            actions0[0][experience.action] = experience.value + discount_factor * np.max(actions1)

            X = np.concatenate((X, np.reshape(experience.state0, (1, self.state_size))), axis=0)
            Y = np.concatenate((Y, actions0), axis=0)

        # feed_dict = {self.state_input: X, self.expected: Y, self.stddev: 0.01}
        feed_dict = {self.state_input: X, self.expected: Y}
        loss =  math.inf
        i = 0
        while loss > 1 and i < 100:
            i += 1;
            loss, _ = self.sess.run([self.loss, self.run_train], feed_dict=feed_dict)
        return loss
