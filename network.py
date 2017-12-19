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

        self.keep_prob = tf.placeholder_with_default(1.0, [], name='keep_prob')
        self.stddev = tf.placeholder_with_default(0.0, [], name='stddev')
        self.states0 = tf.placeholder(tf.float32, shape=(None, self.state_size), name='states0')
        self.actions = tf.placeholder(tf.float32, shape=(None, 1), name='actions')
        self.states1 = tf.placeholder(tf.float32, shape=(None, self.state_size), name='states1')
        self.values = tf.placeholder(tf.float32, shape=(None, 1), name='values')

        noise_vector0 = tf.random_normal(shape=tf.shape(self.states0), mean=0.0, stddev=self.stddev, dtype=tf.float32)
        noisy_states0 = tf.add(self.states0, noise_vector0)
        noise_vector1 = tf.random_normal(shape=tf.shape(self.states1), mean=0.0, stddev=self.stddev, dtype=tf.float32)
        noisy_states1 = tf.add(self.states1, noise_vector1)

        units = 8

        value_hidden0 = tf.layers.dense(inputs=noisy_states1, units=units, activation=tf.nn.relu)
        value_dropout0 = tf.nn.dropout(value_hidden0, self.keep_prob)
        value_hidden1 = tf.layers.dense(inputs=value_dropout0, units=units, activation=tf.nn.relu)
        value_dropout1 = tf.nn.dropout(value_hidden1, self.keep_prob)
        self.value_prediction = tf.layers.dense(inputs=value_dropout1, units=1)
        self.value_loss = tf.reduce_mean(tf.losses.mean_squared_error(self.values, self.value_prediction))
        self.value_run_train = tf.train.AdagradOptimizer(.1).minimize(self.value_loss)

        state_hidden0 = tf.concat([noisy_states0, self.actions], axis=1)
        state_dropout0 = tf.nn.dropout(state_hidden0, self.keep_prob)
        state_hidden1 = tf.layers.dense(inputs=state_dropout0, units=units, activation=tf.nn.relu)
        state_dropout1 = tf.nn.dropout(state_hidden1, self.keep_prob)
        self.state_prediction = tf.layers.dense(inputs=state_dropout1, units=self.state_size)
        self.state_loss = tf.reduce_mean(tf.losses.mean_squared_error(self.states1, self.state_prediction))
        self.state_run_train = tf.train.AdagradOptimizer(.1).minimize(self.state_loss)

        dqn_hidden0 = tf.layers.dense(inputs=noisy_states0, units=units, activation=tf.nn.relu)
        dqn_dropout0 = tf.nn.dropout(dqn_hidden0, self.keep_prob)
        dqn_hidden1 = tf.layers.dense(inputs=dqn_dropout0, units=units, activation=tf.nn.relu)
        dqn_dropout1 = tf.nn.dropout(dqn_hidden1, self.keep_prob)
        self.dqn_prediction = tf.layers.dense(inputs=dqn_dropout1, units=self.action_size)
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

    def state_run(self, states, actions):
        return self.sess.run(self.state_prediction, feed_dict={self.states0: states, self.actions: actions})

    def value_run(self, states):
        return self.sess.run(self.value_prediction, feed_dict={self.states1: states})

    def dqn_run(self, states):
        return self.sess.run(self.dqn_prediction, feed_dict={self.states0: states})

    def value_train(self, experiences, offline):
        states0 = np.array([], dtype=np.float).reshape(0, self.state_size)
        actions = np.array([], dtype=np.float).reshape(0, 1)
        states1 = np.array([], dtype=np.float).reshape(0, self.state_size)
        values = np.array([], dtype=np.float).reshape(0, 1)

        training_count = 10
        training_data = experiences.get()
        if len(training_data) > training_count:
            if offline:
                training_experiences = np.random.choice(training_data, training_count)
            else:
                training_experiences = np.random.choice(training_data, training_count/2)
                training_experiences = np.concatenate((training_experiences, training_data[-training_count/2:]), axis=0)
        else:
            training_experiences = training_data

        for experience in training_experiences:
            state1 = experience.state0
            value = experience.value

            states1 = np.concatenate((states1, np.reshape(state1, (1, self.state_size))), axis=0)
            values = np.concatenate((values, np.reshape(value, (1, 1))), axis=0)

        feed_dict = {self.states1: states1, self.values: values, self.keep_prob: 0.99, self.stddev: 0.01}
        loss = math.inf
        i = 0
        while loss > .001 and i < 1000:
            i += 1
            loss, _ = self.sess.run([self.value_loss, self.value_run_train], feed_dict=feed_dict)
        return loss

    def state_train(self, experiences, offline):
        states0 = np.array([], dtype=np.float).reshape(0, self.state_size)
        actions = np.array([], dtype=np.float).reshape(0, 1)
        states1 = np.array([], dtype=np.float).reshape(0, self.state_size)

        training_count = 10
        training_data = experiences.get()
        if len(training_data) > training_count:
            if offline:
                training_experiences = np.random.choice(training_data, training_count)
            else:
                training_experiences = np.random.choice(training_data, training_count/2)
                training_experiences = np.concatenate((training_experiences, training_data[-training_count/2:]), axis=0)
        else:
            training_experiences = training_data

        for experience in training_experiences:
            state0 = experience.state0
            action = experience.action
            state1 = experience.state1

            states0 = np.concatenate((states0, np.reshape(state0, (1, self.state_size))), axis=0)
            actions = np.concatenate((actions, np.reshape(action, (1, 1))), axis=0)
            states1 = np.concatenate((states1, np.reshape(state1, (1, self.state_size))), axis=0)

        feed_dict = {self.states0: states0, self.actions: actions, self.states1: states1, self.keep_prob: 0.99, self.stddev: 0.01}
        loss = math.inf
        i = 0
        while loss > .001 and i < 1000:
            i += 1;
            loss, _ = self.sess.run([self.state_loss, self.state_run_train], feed_dict=feed_dict)
        return loss

    def dqn_train(self, experiences, offline):
        X = np.array([], dtype=np.float).reshape(0, self.states0.shape[1])
        Y = np.array([], dtype=np.float).reshape(0, self.action_size)

        training_count = 10
        training_data = experiences.get()
        if len(training_data) > training_count:
            if offline:
                training_experiences = np.random.choice(training_data, training_count)
            else:
                training_experiences = np.random.choice(training_data, training_count/2)
                training_experiences = np.concatenate((training_experiences, training_data[-training_count/2:]), axis=0)
        else:
            training_experiences = training_data

        for experience in training_experiences:
            state0 = experience.state0
            action = experience.action

            for i in range(10):
                states0 = [state0] * self.action_size
                actions = np.arange(self.action_size).reshape((self.action_size, 1))
                states1 = self.state_run(states0, actions)
                values = self.value_run(states1)

                actions0 = self.dqn_run([state0])
                actions1 = self.dqn_run(states1)
                action = [np.argmax(actions0)]
                discount_factor = .99
                actions0[0] = [values[x] + discount_factor * np.max(actions1[x]) for x in range(self.action_size)]

                X = np.concatenate((X, np.reshape(state0, (1, self.state_size))), axis=0)
                Y = np.concatenate((Y, actions0), axis=0)
                state0 = states1[action][0]

        feed_dict = {self.states0: X, self.dqn_expected: Y, self.keep_prob: 0.99, self.stddev: 0.01}
        loss = math.inf
        i = 0
        while loss > .001 and i < 1000:
            i += 1;
            loss, _ = self.sess.run([self.dqn_loss, self.dqn_run_train], feed_dict=feed_dict)
        return loss