import tensorflow as tf
import numpy as np
import os.path
import math

def sigmoid(v):
    if v < -700:
        return 0
    else:
        return (1.0 / (1.0 + math.exp(-v)) - 0.5) * 2.0

class Model:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size

        self.stddev = tf.placeholder_with_default(0.0, [])
        self.states0 = tf.placeholder(tf.float32, shape=(None, state_size))
        self.actions = tf.placeholder(tf.float32, shape=(None, 1))
        self.states1 = tf.placeholder(tf.float32, shape=(None, self.state_size))
        self.values = tf.placeholder(tf.float32, shape=(None, 1))

        noise_vector = tf.random_normal(shape=tf.shape(self.states0), mean=0.0, stddev=self.stddev, dtype=tf.float32)
        noisy_states0 = tf.add(self.states0, noise_vector)

        units = 8
        model_hidden0 = tf.concat([noisy_states0, self.actions], axis=1)
        model_hidden1 = tf.layers.dense(inputs=model_hidden0, units=units, activation=tf.nn.tanh)
        model_hidden2 = tf.layers.dense(inputs=model_hidden1, units=units, activation=tf.nn.tanh)
        # model_hidden3 = tf.layers.dense(inputs=model_hidden2, units=units, activation=tf.nn.tanh)
        self.model_prediction = tf.layers.dense(inputs=model_hidden2, units=self.state_size + 1)
        model_expected = tf.concat([self.states1, self.values], axis=1)
        self.model_loss = tf.reduce_mean(tf.losses.mean_squared_error(model_expected, self.model_prediction))
        self.model_run_train = tf.train.AdagradOptimizer(.1).minimize(self.model_loss)
        self.model_prediction_states1 = tf.slice(self.model_prediction, [0, 0], [-1, self.state_size])
        self.model_prediction_values = tf.slice(self.model_prediction, [0, self.state_size], [-1, 1])

        dqn_hidden1 = tf.layers.dense(inputs=self.states0, units=units, activation=tf.nn.tanh)
        dqn_hidden2 = tf.layers.dense(inputs=dqn_hidden1, units=units, activation=tf.nn.tanh)
        # dqn_hidden3 = tf.layers.dense(inputs=dqn_hidden2, units=units, activation=tf.nn.tanh)
        self.dqn_prediction = tf.layers.dense(inputs=dqn_hidden2, units=self.action_size)
        self.dqn_expected = tf.placeholder(tf.float32, shape=(None, self.action_size))
        self.dqn_loss = tf.reduce_mean(tf.losses.mean_squared_error(self.dqn_expected, self.dqn_prediction))
        self.dqn_run_train = tf.train.AdagradOptimizer(.1).minimize(self.dqn_loss)

        self.sess = tf.Session()
        self.sess.run(tf.global_variables_initializer())

        if os.path.exists('graph/graph.meta'):
                print("loading training data")
                saver = tf.train.Saver()
                saver.restore(self.sess, 'graph/graph')

    def save(self):
        saver = tf.train.Saver()
        saver.save(self.sess, 'graph/graph')

    def model_run(self, states, actions):
        return self.sess.run([self.model_prediction_states1, self.model_prediction_values], feed_dict={self.states0: states, self.actions: actions})

    def dqn_run(self, states):
        return self.sess.run(self.dqn_prediction, feed_dict={self.states0: states})

    def model_train(self, experiences):
        states0 = np.array([], dtype=np.float).reshape(0, self.state_size)
        actions = np.array([], dtype=np.float).reshape(0, 1)
        states1 = np.array([], dtype=np.float).reshape(0, self.state_size)
        values = np.array([], dtype=np.float).reshape(0, 1)

        training_data = experiences.get()

        if (len(experiences.get()) > 100):
            training_experiences = np.random.choice(training_data, 50)
            training_experiences = np.concatenate((training_experiences, training_data[-50:]), axis=0)
        else:
            training_experiences = training_data

        for experience in training_experiences:
            state0 = experience.state0
            action = experience.action
            state1 = experience.state1
            value = experience.value

            states0 = np.concatenate((states0, np.reshape(state0, (1, self.state_size))), axis=0)
            actions = np.concatenate((actions, np.reshape(action, (1, 1))), axis=0)
            states1 = np.concatenate((states1, np.reshape(state1, (1, self.state_size))), axis=0)
            values = np.concatenate((values, np.reshape(value, (1, 1))), axis=0)

        feed_dict = {self.states0: states0, self.actions: actions, self.states1: states1, self.values: values, self.stddev: 0.025}
        loss = math.inf
        i = 0
        while loss > .01 and i < 1000:
            i += 1;
            loss, _ = self.sess.run([self.model_loss, self.model_run_train], feed_dict=feed_dict)
        return loss

    def dqn_train(self, experiences):
        X = np.array([], dtype=np.float).reshape(0, self.states0.shape[1])
        Y = np.array([], dtype=np.float).reshape(0, self.action_size)

        training_data = experiences.get()

        experience = np.random.choice(training_data, 1)[0]

        state0 = experience.state0
        action = experience.action

        states1, values = self.model_run([state0], [action])
        print(experience.state1 - states1[0])

        for i in range(10):
            states1, values = self.model_run([state0], [action])
            state1 = states1[0]
            value = values[0][0]

            actions0 = self.dqn_run([state0])
            actions1 = self.dqn_run([state1])
            action = [np.argmax(actions0)]
            discount_factor = .95
            actions0[0][action] = value + discount_factor * np.max(actions1)

            X = np.concatenate((X, np.reshape(state0, (1, self.state_size))), axis=0)
            Y = np.concatenate((Y, actions0), axis=0)
            state0 = state1

        feed_dict = {self.states0: X, self.dqn_expected: Y}
        loss = math.inf
        i = 0
        while loss > .01 and i < 1000:
            i += 1;
            loss, _ = self.sess.run([self.dqn_loss, self.dqn_run_train], feed_dict=feed_dict)
        return loss