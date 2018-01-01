import tensorflow as tf
import numpy as np
import os.path
import math
import time

class Model:
    def __init__(self, state_size, action_size):

        self.state_size = state_size
        self.action_size = action_size

        self.states0 = tf.placeholder(tf.float32, shape=(None, self.state_size), name='states0')
        self.actions = tf.placeholder(tf.float32, shape=(None, 1), name='actions')
        self.states1 = tf.placeholder(tf.float32, shape=(None, self.state_size), name='states1')
        self.values = tf.placeholder(tf.float32, shape=(None, 1), name='values')

        self.regularizer_scale = tf.placeholder_with_default(0.0, [])

        state_max = tf.get_variable("state_max", shape=(self.state_size), initializer=tf.constant_initializer(-math.inf))
        states_max = tf.concat([self.states0, [state_max]], axis=0)
        state_max = state_max.assign(tf.reduce_max(states_max, axis=0))

        state_min = tf.get_variable("state_min", shape=(self.state_size), initializer=tf.constant_initializer(math.inf))
        states_min = tf.concat([self.states0, [state_min]], axis=0)
        state_min = state_min.assign(tf.reduce_min(states_min, axis=0))

        diff = tf.subtract(state_max, state_min)
        diff = tf.where(tf.equal(diff, 0.0), tf.ones_like(diff), diff)

        normal_states0 = tf.divide(tf.subtract(self.states0, state_min), diff)

        units = 64

        regularizer = tf.contrib.layers.l1_regularizer(self.regularizer_scale)

        model_input = tf.concat([normal_states0, self.actions], axis=1)

        value_hidden0 = tf.layers.dense(inputs=model_input, units=units, activation=tf.nn.relu, kernel_regularizer=regularizer)
        value_hidden1 = tf.layers.dense(inputs=value_hidden0, units=units, activation=tf.nn.relu, kernel_regularizer=regularizer)
        value_hidden2 = tf.layers.dense(inputs=value_hidden1, units=units, activation=tf.nn.relu, kernel_regularizer=regularizer)
        value_hidden3 = tf.layers.dense(inputs=value_hidden2, units=units, activation=tf.nn.relu, kernel_regularizer=regularizer)
        self.value_prediction = tf.layers.dense(inputs=value_hidden3, units=1)
        self.value_loss = tf.reduce_mean(tf.losses.mean_squared_error(self.values, self.value_prediction))
        self.value_run_train = tf.train.AdagradOptimizer(.1).minimize(self.value_loss)

        state_hidden0 = tf.layers.dense(inputs=model_input, units=units, activation=tf.nn.relu, kernel_regularizer=regularizer)
        state_hidden1 = tf.layers.dense(inputs=state_hidden0, units=units, activation=tf.nn.relu, kernel_regularizer=regularizer)
        state_hidden2 = tf.layers.dense(inputs=state_hidden1, units=units, activation=tf.nn.relu, kernel_regularizer=regularizer)
        state_hidden3 = tf.layers.dense(inputs=state_hidden2, units=units, activation=tf.nn.relu, kernel_regularizer=regularizer)
        self.state_prediction = tf.layers.dense(inputs=state_hidden3, units=self.state_size)
        self.state_loss = tf.reduce_mean(tf.losses.mean_squared_error(self.states1, self.state_prediction))
        self.state_run_train = tf.train.AdagradOptimizer(.1).minimize(self.state_loss)

        dqn_hidden0 = tf.layers.dense(inputs=normal_states0, units=units, activation=tf.nn.relu, kernel_regularizer=regularizer)
        dqn_hidden1 = tf.layers.dense(inputs=dqn_hidden0, units=units, activation=tf.nn.relu, kernel_regularizer=regularizer)
        dqn_hidden2 = tf.layers.dense(inputs=dqn_hidden1, units=units, activation=tf.nn.relu, kernel_regularizer=regularizer)
        dqn_hidden3 = tf.layers.dense(inputs=dqn_hidden2, units=units, activation=tf.nn.relu, kernel_regularizer=regularizer)
        self.dqn_prediction = tf.layers.dense(inputs=dqn_hidden3, units=self.action_size)
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
        return self.sess.run([self.state_prediction, self.value_prediction], feed_dict={self.states0: states, self.actions: actions})

    def dqn_run(self, states):
        return self.sess.run(self.dqn_prediction, feed_dict={self.states0: states})

    def model_train(self, experiences):
        states0 = np.array([], dtype=np.float).reshape(0, self.state_size)
        actions = np.array([], dtype=np.float).reshape(0, 1)
        states1 = np.array([], dtype=np.float).reshape(0, self.state_size)
        values = np.array([], dtype=np.float).reshape(0, 1)

        training_data = experiences.get()

        training_count = 500
        training_experiences = np.random.choice(training_data, training_count)

        for experience in training_experiences:
            state0 = experience.state0
            action = experience.action
            state1 = experience.state1
            value = experience.value

            states0 = np.concatenate((states0, np.reshape(state0, (1, self.state_size))), axis=0)
            actions = np.concatenate((actions, np.reshape(action, (1, 1))), axis=0)
            states1 = np.concatenate((states1, np.reshape(state1, (1, self.state_size))), axis=0)
            values = np.concatenate((values, np.reshape(value, (1, 1))), axis=0)

        feed_dict = {self.states0: states0, self.actions: actions, self.states1: states1, self.values: values, self.regularizer_scale: 0.1}
        start = time.time()
        while (time.time() - start) < 1:
            state_loss, _, value_loss, _ = self.sess.run([self.state_loss, self.state_run_train, self.value_loss, self.value_run_train], feed_dict=feed_dict)
        return value_loss, state_loss

    def dqn_train(self, experiences):
        discount = 0.5

        states0 = np.array([], dtype=np.float).reshape(0, self.states0.shape[1])
        expected = np.array([], dtype=np.float).reshape(0, self.action_size)

        training_data = experiences.get()

        start = time.time()
        while (time.time() - start) < 1:
            states0 = np.array([], dtype=np.float).reshape(0, self.states0.shape[1])
            expected = np.array([], dtype=np.float).reshape(0, self.action_size)

            experience = np.random.choice(training_data)

            state0 = experience.state0
            state1 = experience.state1
            action = experience.action
            value = experience.value

            [actions0, actions1] = self.dqn_run([state0, state1])
            action = np.argmax(actions0)
            actions0[action] = (1 - discount) * value + discount * np.max(actions1)
            states0 = np.concatenate((states0, np.reshape(state0, (1, self.state_size))), axis=0)
            expected = np.concatenate((expected, np.reshape(actions0, (1, self.action_size))), axis=0)

            for i in range(10):
                states = [state0] * self.action_size
                actions = np.arange(self.action_size).reshape((self.action_size, 1))
                states1, values = self.model_run(states, actions)

                actions0 = self.dqn_run(states)
                actions1 = self.dqn_run(states1)
                action = [np.argmax(actions0)]
                actions0 = [(1 - discount) * values[x] + discount * np.max(actions1[x]) for x in range(self.action_size)]

                states0 = np.concatenate((states0, np.reshape(state0, (1, self.state_size))), axis=0)
                expected = np.concatenate((expected, np.reshape(actions0, (1, self.action_size))), axis=0)
                state0 = states1[action][0]

            feed_dict = {self.states0: states0, self.dqn_expected: expected, self.regularizer_scale: 0.1}
            loss, _ = self.sess.run([self.dqn_loss, self.dqn_run_train], feed_dict=feed_dict)
            while (time.time() - start) < 1 and loss > 0.01:
                loss, _ = self.sess.run([self.dqn_loss, self.dqn_run_train], feed_dict=feed_dict)
        return loss