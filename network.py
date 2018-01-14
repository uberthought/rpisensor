import tensorflow as tf
import numpy as np
import os.path
import math
import time

def createHidden(input_layer, units, name):
        input_units = int(input_layer.shape[1])
        with tf.name_scope(name):
            weights = tf.Variable(tf.truncated_normal([input_units, units], stddev=1.0/math.sqrt(float(input_units)), dtype=tf.float32), name='weights')
            biases = tf.Variable(tf.zeros([units], dtype=tf.float32), name='biases')
            result = tf.matmul(input_layer, weights)
            result = tf.nn.relu(result)
            result = tf.add(result, biases)
            if input_units == units:
                result = tf.add(input_layer, result)
            return result

def createOutput(input_layer, units, name):
        input_units = int(input_layer.shape[1])
        with tf.name_scope(name):
            weights = tf.Variable(tf.truncated_normal([input_units, units], stddev=1.0/math.sqrt(float(input_units)), dtype=tf.float32), name='weights')
            biases = tf.Variable(tf.zeros([units], dtype=tf.float32), name='biases')
            result = tf.matmul(input_layer, weights)
            result = tf.add(result, biases)
            if input_units == units:
                result = tf.add(input_layer, result)
            return result

class Model:
    state_size = 4
    action_size = 4

    def __init__(self):

        self.states0 = tf.placeholder(tf.float32, shape=(None, Model.state_size), name='states0')
        self.actions = tf.placeholder(tf.float32, shape=(None, Model.action_size), name='actions')
        self.states1 = tf.placeholder(tf.float32, shape=(None, Model.state_size), name='states1')
        self.values = tf.placeholder(tf.float32, shape=(None, 1), name='values')

        units = 32

        model_input = tf.concat([self.states0, self.actions], axis=1, name='model_input')
        model_output = tf.concat([self.states1, self.values], axis=1, name='model_output')
        hidden = model_input
        for i in range(4):
            hidden = createHidden(hidden, units, 'model_hidden_' + str(i))
        self.model_prediction = createOutput(hidden, Model.state_size + 1, 'model_prediction')
        self.model_loss = tf.reduce_mean(tf.losses.mean_squared_error(model_output, self.model_prediction))
        self.model_run_train = tf.train.AdagradOptimizer(.1).minimize(self.model_loss)
        self.value_prediction = tf.slice(self.model_prediction, [0, Model.state_size], [-1, 1], name='value_prediction')
        self.state_prediction = tf.slice(self.model_prediction, [0, 0], [-1, Model.state_size], name='state_prediction')

        hidden = self.states0
        for i in range(4):
            hidden = createHidden(hidden, units, 'dqn_hidden_' + str(i))
        self.dqn_prediction = createOutput(hidden, Model.action_size, 'dqn_prediction')
        self.dqn_expected = tf.placeholder(tf.float32, shape=(None, self.action_size))
        self.dqn_loss = tf.reduce_mean(tf.losses.mean_squared_error(self.dqn_expected, self.dqn_prediction))
        self.dqn_run_train = tf.train.AdagradOptimizer(.1).minimize(self.dqn_loss)
        self.dqn_action = tf.argmax(self.dqn_prediction, axis=1)

        self.sess = tf.Session()

        self.summary_writer = tf.summary.FileWriter('./graph', self.sess.graph)
        model_loss_summary = tf.summary.scalar('value loss', self.model_loss)
        # model_expected_summary = tf.summary.histogram('value expected', self.values)
        # model_predicted_summary = tf.summary.histogram('value prediction', self.model_prediction)
        # model_hidden0_summary = tf.summary.histogram('model hidden 0', model_hidden0)
        # model_hidden1_summary = tf.summary.histogram('model hidden 1', model_hidden1)
        self.model_summary = tf.summary.merge([model_loss_summary])

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
        states0, actions, values, states1 = experiences.get()

        size = len(states0)
        if size == 0:
            return math.inf
        if size > 500:
            size = 500

        p = np.random.exponential(size=size)
        p = np.sort(p)
        p /= np.sum(p)

        i = np.random.choice(range(size), size, p=p)
        states0 = states0[i]
        actions = actions[i]
        values = values[i]
        states1 = states1[i]

        feed_dict = {self.states0: states0, self.actions: actions, self.states1: states1, self.values: values}
        # start = time.time()
        for i in range(200):
            model_loss, _, summary = self.sess.run([self.model_loss, self.model_run_train, self.model_summary], feed_dict=feed_dict)
            self.summary_writer.add_summary(summary)
        # print(time.time() - start)
        return model_loss

    def dqn_train(self, experiences):
        discount = 0.5

        states0 = np.array([], dtype=np.float).reshape(0, self.states0.shape[1])
        expected = np.array([], dtype=np.float).reshape(0, self.action_size)

        states0, actions, values, states1 = experiences.get()
    
        size = len(states0)
        if size == 0:
            return math.inf

        p = np.random.exponential(size=size)
        p = np.sort(p)
        p /= np.sum(p)

        X = np.array([], dtype=np.float).reshape(0, self.states0.shape[1])
        Y = np.array([], dtype=np.float).reshape(0, self.action_size)

        for k in range(20):
            i = np.random.choice(range(size), p=p)
            state0 = states0[i]
            value = values[i]
            state1 = states1[i]

            [actions0, actions1] = self.dqn_run([state0, state1])
            action = np.argmax(actions0)
            actions0[action] = (1 - discount) * value + discount * np.max(actions1)
            X = np.concatenate((X, np.reshape(state0, (1, Model.state_size))), axis=0)
            Y = np.concatenate((Y, np.reshape(actions0, (1, self.action_size))), axis=0)

            hstate0 = state0
            for i in range(2):
                hstates0 = [hstate0] * self.action_size
                hactions = np.zeros((self.action_size, self.action_size))
                for j in range(self.action_size):
                    hactions[j][j] = 1
                hstates1, hvalues = self.model_run(hstates0, hactions)

                hactions1 = self.dqn_run(hstates1)
                haction = [self.dqn_run_action(hstates0)]
                hactions0 = [(1 - discount) * hvalues[x] + discount * np.max(hactions1[x]) for x in range(self.action_size)]

                X = np.concatenate((X, np.reshape(hstate0, (1, Model.state_size))), axis=0)
                Y = np.concatenate((Y, np.reshape(hactions0, (1, self.action_size))), axis=0)
                hstate0 = hstates1[haction][0]

        feed_dict = {self.states0: X, self.dqn_expected: Y}
        loss, _ = self.sess.run([self.dqn_loss, self.dqn_run_train], feed_dict=feed_dict)

        # start = time.time()
        for i in range(100):
            loss, _, summary = self.sess.run([self.dqn_loss, self.dqn_run_train, self.dqn_summary], feed_dict=feed_dict)
            self.summary_writer.add_summary(summary)
        # print(time.time() - start)

        return loss