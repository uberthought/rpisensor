import tensorflow as tf
import numpy as np
import os.path
import math
import time

def createHidden(input_layer, units, name):
        input_units = int(input_layer.shape[1])
        with tf.name_scope(name):
            weights = tf.Variable(tf.truncated_normal([input_units, units], stddev=1.0/math.sqrt(float(input_units))), name='weights')
            biases = tf.Variable(tf.zeros([units]), name='biases')
            return tf.nn.relu(tf.matmul(input_layer, weights) + biases)

def createOutput(input_layer, units, name):
        input_units = int(input_layer.shape[1])
        with tf.name_scope(name):
            weights = tf.Variable(tf.truncated_normal([input_units, units], stddev=1.0/math.sqrt(float(input_units))), name='weights')
            biases = tf.Variable(tf.zeros([units]), name='biases')
            return tf.matmul(input_layer, weights) + biases

class Model:
    state_size = 2
    action_size = 4

    def __init__(self):

        self.states0 = tf.placeholder(tf.float32, shape=(None, Model.state_size), name='states0')
        self.actions = tf.placeholder(tf.float32, shape=(None, Model.action_size), name='actions')
        self.states1 = tf.placeholder(tf.float32, shape=(None, Model.state_size), name='states1')
        self.values = tf.placeholder(tf.float32, shape=(None, 1), name='values')
        self.regularizer_scale = tf.placeholder_with_default(0.01, [])

        units = 32

        model_input = tf.concat([self.states0, self.actions], axis=1, name='model_input')
        model_output = tf.concat([self.states1, self.values], axis=1, name='model_output')
        regularizer = tf.contrib.layers.l2_regularizer(self.regularizer_scale)

        model_hidden0 = createHidden(model_input, units, 'model_hidden_0')
        model_hidden1 = createHidden(model_hidden0, units, 'model_hidden_1')
        model_hidden2 = createHidden(model_hidden1, units, 'model_hidden_2')
        model_hidden3 = createHidden(model_hidden2, units, 'model_hidden_3')
        self.model_prediction = createOutput(model_hidden3, Model.state_size + 1, 'model_prediction')
        self.model_loss = tf.reduce_mean(tf.losses.mean_squared_error(model_output, self.model_prediction))
        self.model_run_train = tf.train.AdagradOptimizer(.1).minimize(self.model_loss)
        self.value_prediction = tf.slice(self.model_prediction, [0, Model.state_size], [-1, 1], name='value_prediction')
        self.state_prediction = tf.slice(self.model_prediction, [0, 0], [-1, Model.state_size], name='state_prediction')

        dqn_hidden0 = createHidden(self.states0, units, 'dqn_hidden_0')
        dqn_hidden1 = createHidden(dqn_hidden0, units, 'dqn_hidden_1')
        dqn_hidden2 = createHidden(dqn_hidden1, units, 'dqn_hidden_2')
        dqn_hidden3 = createHidden(dqn_hidden2, units, 'dqn_hidden_3')
        self.dqn_prediction = createOutput(dqn_hidden3, Model.action_size, 'dqn_prediction')
        self.dqn_expected = tf.placeholder(tf.float32, shape=(None, self.action_size))
        self.dqn_loss = tf.reduce_mean(tf.losses.mean_squared_error(self.dqn_expected, self.dqn_prediction))
        self.dqn_run_train = tf.train.AdagradOptimizer(.1).minimize(self.dqn_loss)
        self.dqn_action = tf.argmax(self.dqn_prediction, axis=1)

        self.sess = tf.Session()

        self.summary_writer = tf.summary.FileWriter('./graph', self.sess.graph)
        model_loss_summary = tf.summary.scalar('value loss', self.model_loss)
        # model_expected_summary = tf.summary.histogram('value expected', self.values)
        # model_predicted_summary = tf.summary.histogram('value prediction', self.model_prediction)
        model_hidden0_summary = tf.summary.histogram('model hidden 0', model_hidden0)
        model_hidden1_summary = tf.summary.histogram('model hidden 1', model_hidden1)
        self.model_summary = tf.summary.merge([model_loss_summary, model_hidden0_summary, model_hidden1_summary])

        dqn_loss_summary = tf.summary.scalar('dqn loss', self.dqn_loss)
        self.dqn_summary = tf.summary.merge([dqn_loss_summary])

        self.sess.run(tf.global_variables_initializer())

        if os.path.exists('graph/graph.meta'):
                print("loading training data")
                saver = tf.train.Saver()
                saver.restore(self.sess, 'graph/graph')

    def save(self):
        saver = tf.train.Saver()
        saver.save(self.sess, 'graph/graph')
        self.summary_writer.flush()

    def model_run(self, states, actions):
        return self.sess.run([self.state_prediction, self.value_prediction], feed_dict={self.states0: states, self.actions: actions})

    def dqn_run(self, states):
        return self.sess.run(self.dqn_prediction, feed_dict={self.states0: states})

    def dqn_run_action(self, states):
        return self.sess.run(self.dqn_action, feed_dict={self.states0: states})[0]

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
        while (time.time() - start) < 3:
            model_loss, _, summary = self.sess.run([self.model_loss, self.model_run_train, self.model_summary], feed_dict=feed_dict)
            self.summary_writer.add_summary(summary)
        return model_loss

    def dqn_train(self, experiences):
        discount = 0.1

        states0 = np.array([], dtype=np.float).reshape(0, self.states0.shape[1])
        expected = np.array([], dtype=np.float).reshape(0, self.action_size)

        training_data = experiences.get()
        if training_data is None:
            return math.inf

        start = time.time()
        while (time.time() - start) < 1:
            states0 = np.array([], dtype=np.float).reshape(0, self.states0.shape[1])
            expected = np.array([], dtype=np.float).reshape(0, self.action_size)

            for k in range(20):
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

                for i in range(5):
                    states = [state0] * self.action_size
                    actions = np.zeros((self.action_size, self.action_size))
                    for j in range(self.action_size):
                        actions[j][j] = 1
                    states1, values = self.model_run(states, actions)

                    actions1 = self.dqn_run(states1)
                    action = [self.dqn_run_action(states)]
                    actions0 = [(1 - discount) * values[x] + discount * np.max(actions1[x]) for x in range(self.action_size)]

                    states0 = np.concatenate((states0, np.reshape(state0, (1, Model.state_size))), axis=0)
                    expected = np.concatenate((expected, np.reshape(actions0, (1, self.action_size))), axis=0)
                    state0 = states1[action][0]

            feed_dict = {self.states0: states0, self.dqn_expected: expected}
            loss, _ = self.sess.run([self.dqn_loss, self.dqn_run_train], feed_dict=feed_dict)
            while (time.time() - start) < 1 and loss > 0.01:
                loss, _, summary = self.sess.run([self.dqn_loss, self.dqn_run_train, self.dqn_summary], feed_dict=feed_dict)
                self.summary_writer.add_summary(summary)

        return loss