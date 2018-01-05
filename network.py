import tensorflow as tf
import numpy as np
import os.path
import math
import time

class Model:
    state_size = 2
    action_size = 4

    def __init__(self):

        self.states0 = tf.placeholder(tf.float32, shape=(None, Model.state_size), name='states0')
        self.actions = tf.placeholder(tf.float32, shape=(None, Model.action_size), name='actions')
        self.states1 = tf.placeholder(tf.float32, shape=(None, Model.state_size), name='states1')
        self.values = tf.placeholder(tf.float32, shape=(None, 1), name='values')

        units = 32

        model_input = tf.concat([self.states0, self.actions], axis=1)

        value_hidden0 = tf.layers.dense(inputs=model_input, units=units, activation=tf.nn.relu)
        value_hidden1 = tf.layers.dense(inputs=value_hidden0, units=units, activation=tf.nn.relu)
        self.value_prediction = tf.layers.dense(inputs=value_hidden1, units=1)
        self.value_loss = tf.reduce_mean(tf.losses.mean_squared_error(self.values, self.value_prediction))
        self.value_run_train = tf.train.AdagradOptimizer(.1).minimize(self.value_loss)

        state_hidden0 = tf.layers.dense(inputs=model_input, units=units, activation=tf.nn.relu)
        state_hidden1 = tf.layers.dense(inputs=state_hidden0, units=units, activation=tf.nn.relu)
        self.state_prediction = tf.layers.dense(inputs=state_hidden1, units=Model.state_size)
        self.state_loss = tf.reduce_mean(tf.losses.mean_squared_error(self.states1, self.state_prediction))
        self.state_run_train = tf.train.AdagradOptimizer(.1).minimize(self.state_loss)

        dqn_hidden0 = tf.layers.dense(inputs=self.states0, units=units, activation=tf.nn.relu)
        dqn_hidden1 = tf.layers.dense(inputs=dqn_hidden0, units=units, activation=tf.nn.relu)
        self.dqn_prediction = tf.layers.dense(inputs=dqn_hidden1, units=self.action_size)
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
        states0 = np.array([], dtype=np.float).reshape(0, Model.state_size)
        actions = np.array([], dtype=np.float).reshape(0, self.action_size)
        states1 = np.array([], dtype=np.float).reshape(0, Model.state_size)
        values = np.array([], dtype=np.float).reshape(0, 1)

        training_data = experiences.get()
        if training_data is None:
            return math.inf

        training_count = 500
        training_experiences = np.random.choice(training_data, training_count)

        for experience in training_experiences:
            state0 = experience.state0
            action = experience.action
            state1 = experience.state1
            value = experience.value

            states0 = np.concatenate((states0, np.reshape(state0, (1, Model.state_size))), axis=0)
            actions = np.concatenate((actions, np.reshape(action, (1, self.action_size))), axis=0)
            states1 = np.concatenate((states1, np.reshape(state1, (1, Model.state_size))), axis=0)
            values = np.concatenate((values, np.reshape(value, (1, 1))), axis=0)

        feed_dict = {self.states0: states0, self.actions: actions, self.states1: states1, self.values: values}
        start = time.time()
        while (time.time() - start) < 2:
            state_loss, _, value_loss, _ = self.sess.run([self.state_loss, self.state_run_train, self.value_loss, self.value_run_train], feed_dict=feed_dict)
        return value_loss, state_loss

    def dqn_train(self, experiences):
        discount = 0.3

        states0 = np.array([], dtype=np.float).reshape(0, self.states0.shape[1])
        expected = np.array([], dtype=np.float).reshape(0, self.action_size)

        training_data = experiences.get()
        if training_data is None:
            return math.inf

        start = time.time()
        while (time.time() - start) < 1:
            states0 = np.array([], dtype=np.float).reshape(0, self.states0.shape[1])
            expected = np.array([], dtype=np.float).reshape(0, self.action_size)

            for k in range(10):
                experience = np.random.choice(training_data)

                state0 = experience.state0
                state1 = experience.state1
                action = experience.action
                value = experience.value

                [actions0, actions1] = self.dqn_run([state0, state1])
                action = np.argmax(actions0)
                actions0[action] = (1 - discount) * value + discount * np.max(actions1)
                states0 = np.concatenate((states0, np.reshape(state0, (1, Model.state_size))), axis=0)
                expected = np.concatenate((expected, np.reshape(actions0, (1, self.action_size))), axis=0)

                for i in range(10):
                    states = [state0] * self.action_size
                    actions = np.zeros((self.action_size, self.action_size))
                    for j in range(self.action_size):
                        actions[j][j] = 1
                    states1, values = self.model_run(states, actions)

                    actions0 = self.dqn_run(states)
                    actions1 = self.dqn_run(states1)
                    action = [np.argmax(actions0)]
                    actions0 = [(1 - discount) * values[x] + discount * np.max(actions1[x]) for x in range(self.action_size)]

                    states0 = np.concatenate((states0, np.reshape(state0, (1, Model.state_size))), axis=0)
                    expected = np.concatenate((expected, np.reshape(actions0, (1, self.action_size))), axis=0)
                    state0 = states1[action][0]

            feed_dict = {self.states0: states0, self.dqn_expected: expected}
            loss, _ = self.sess.run([self.dqn_loss, self.dqn_run_train], feed_dict=feed_dict)
            while (time.time() - start) < 1 and loss > 0.01:
                loss, _ = self.sess.run([self.dqn_loss, self.dqn_run_train], feed_dict=feed_dict)
        return loss