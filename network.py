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

        self.states0 = tf.placeholder(tf.float32, shape=(None, self.state_size), name='states0')
        self.actions = tf.placeholder(tf.float32, shape=(None, 1), name='actions')
        self.states1 = tf.placeholder(tf.float32, shape=(None, self.state_size), name='states1')
        self.values = tf.placeholder(tf.float32, shape=(None, 1), name='values')

        units = 4

        model_input = tf.concat([self.states0, self.actions], axis=1)
        model_hidden0 = tf.layers.dense(inputs=model_input, units=units, activation=tf.nn.relu)
        # model_hidden1 = tf.layers.dense(inputs=model_hidden0, units=units, activation=tf.nn.relu)
        # model_hidden2 = tf.layers.dense(inputs=model_hidden0, units=units, activation=tf.nn.relu)
        self.model_prediction = tf.layers.dense(inputs=model_hidden0, units=self.state_size + 1)
        model_expected = tf.concat([self.states1, self.values], axis=1)
        self.model_loss = tf.reduce_mean(tf.losses.mean_squared_error(model_expected, self.model_prediction))
        self.model_run_train = tf.train.AdagradOptimizer(.1).minimize(self.model_loss)
        self.model_prediction_states1 = tf.slice(self.model_prediction, [0, 0], [-1, self.state_size])
        self.model_prediction_values = tf.slice(self.model_prediction, [0, self.state_size], [-1, 1])

        dqn_hidden0 = tf.layers.dense(inputs=self.states0, units=units, activation=tf.nn.relu)
        dqn_hidden1 = tf.layers.dense(inputs=dqn_hidden0, units=units, activation=tf.nn.relu)
        dqn_hidden2 = tf.layers.dense(inputs=dqn_hidden1, units=units, activation=tf.nn.relu)
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

        training_count = 10000
        training_data = experiences.get()
        if len(training_data) > training_count:
            training_experiences = np.random.choice(training_data, training_count)
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

        feed_dict = {self.states0: states0, self.actions: actions, self.states1: states1, self.values: values}
        loss = math.inf
        i = 0
        while loss > .0001 and i < 1000:
            i += 1;
            loss, _ = self.sess.run([self.model_loss, self.model_run_train], feed_dict=feed_dict)
        return loss

    def dqn_train(self, experiences):
        discount_factor = 1

        X = np.array([], dtype=np.float).reshape(0, self.states0.shape[1])
        Y = np.array([], dtype=np.float).reshape(0, self.action_size)

        training_count = 100
        training_data = experiences.get()
        if len(training_data) > training_count:
            training_experiences = np.random.choice(training_data, training_count)
        else:
            training_experiences = training_data

        for experience in training_experiences:
            state0 = experience.state0
            state1 = experience.state1
            action = experience.action
            value = experience.value

            [actions0, actions1] = self.dqn_run([state0, state1])
            action = np.argmax(actions0)
            actions0[action] = value + discount_factor * np.max(actions1)
            X = np.concatenate((X, np.reshape(state0, (1, self.state_size))), axis=0)
            Y = np.concatenate((Y, np.reshape(actions0, (1, self.action_size))), axis=0)

            for i in range(10):
                states0 = [state0] * self.action_size
                actions = np.arange(self.action_size).reshape((self.action_size, 1))
                states1, values = self.model_run(states0, actions)

                actions0 = self.dqn_run(states0)
                actions1 = self.dqn_run(states1)
                action = [np.argmax(actions0)]
                actions0 = [sigmoid(values[x] + discount_factor * np.max(actions1[x])) for x in range(self.action_size)]

                X = np.concatenate((X, np.reshape(state0, (1, self.state_size))), axis=0)
                Y = np.concatenate((Y, np.reshape(actions0, (1, self.action_size))), axis=0)
                state0 = states1[action][0]

        feed_dict = {self.states0: X, self.dqn_expected: Y}
        loss = math.inf
        for j in range(1000):
            loss, _ = self.sess.run([self.dqn_loss, self.dqn_run_train], feed_dict=feed_dict)
        return loss