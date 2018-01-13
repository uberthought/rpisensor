import tensorflow as tf
import numpy as np
import os.path
import math
import time

<<<<<<< HEAD
def createHidden(input_layer, units, name):
        input_units = int(input_layer.shape[1])
        with tf.name_scope(name):
            weights = tf.Variable(tf.truncated_normal([input_units, units], stddev=1.0/math.sqrt(float(input_units)), dtype=tf.float32), name='weights')
            biases = tf.Variable(tf.zeros([units], dtype=tf.float32), name='biases')
            return tf.nn.relu(tf.matmul(input_layer, weights) + biases)

def createOutput(input_layer, units, name):
        input_units = int(input_layer.shape[1])
        with tf.name_scope(name):
            weights = tf.Variable(tf.truncated_normal([input_units, units], stddev=1.0/math.sqrt(float(input_units)), dtype=tf.float32), name='weights')
            biases = tf.Variable(tf.zeros([units], dtype=tf.float32), name='biases')
            return tf.matmul(input_layer, weights) + biases
=======
def exponentialWeightedChoice(data, size):
    p = np.random.exponential(size=len(data))
    p = np.sort(p / np.sum(p))
    return np.random.choice(data, size=size, p=p)
>>>>>>> master

class Model:
    state_size = 4
    action_size = 4

    def __init__(self):

<<<<<<< HEAD
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
=======
        self.states0 = tf.placeholder(tf.float32, shape=(None, self.state_size), name='states0')
        self.actions = tf.placeholder(tf.float32, shape=(None, self.action_size), name='actions')
        self.states1 = tf.placeholder(tf.float32, shape=(None, self.state_size), name='states1')
        self.values = tf.placeholder(tf.float32, shape=(None, self.action_size), name='values')

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
        self.value_prediction = tf.layers.dense(inputs=value_hidden1, units=1)
        self.value_loss = tf.reduce_mean(tf.losses.mean_squared_error(self.values, self.value_prediction))
        self.value_run_train = tf.train.AdagradOptimizer(.1).minimize(self.value_loss)

        state_hidden0 = tf.layers.dense(inputs=model_input, units=units, activation=tf.nn.relu, kernel_regularizer=regularizer)
        state_hidden1 = tf.layers.dense(inputs=state_hidden0, units=units, activation=tf.nn.relu, kernel_regularizer=regularizer)
        self.state_prediction = tf.layers.dense(inputs=state_hidden1, units=self.state_size)
        self.state_loss = tf.reduce_mean(tf.losses.mean_squared_error(self.states1, self.state_prediction))
        self.state_run_train = tf.train.AdagradOptimizer(.1).minimize(self.state_loss)

        dqn_hidden0 = tf.layers.dense(inputs=normal_states0, units=units, activation=tf.nn.relu, kernel_regularizer=regularizer)
        dqn_hidden1 = tf.layers.dense(inputs=dqn_hidden0, units=units, activation=tf.nn.relu, kernel_regularizer=regularizer)
        self.dqn_prediction = tf.layers.dense(inputs=dqn_hidden1, units=self.action_size)
>>>>>>> master
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

        training_count = len(training_data)
        if training_count > 500:
            training_count = 500
        p = np.random.exponential(size=training_count)
        p = np.sort(p)
        p /= np.sum(p)

<<<<<<< HEAD
        training_experiences = np.random.choice(training_data, training_count)
=======
        if len(training_data) <= 0:
            return 0, 0

        # training_experiences = np.random.choice(training_data, 500)
        training_experiences = exponentialWeightedChoice(training_data, 500)
>>>>>>> master

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
<<<<<<< HEAD
        discount = 0.25
=======
        discount = 0.8
>>>>>>> master

        states0 = np.array([], dtype=np.float).reshape(0, self.states0.shape[1])
        expected = np.array([], dtype=np.float).reshape(0, self.action_size)

        training_data = experiences.get()
    
        if training_data is None:
            return math.inf
    
        training_count = len(training_data)
        p = np.random.exponential(size=training_count)
        p /= np.sum(p)

        if len(training_data) <= 0:
            return 0, 0

        start = time.time()
        while (time.time() - start) < 1:
            states0 = np.array([], dtype=np.float).reshape(0, self.states0.shape[1])
            expected = np.array([], dtype=np.float).reshape(0, self.action_size)

<<<<<<< HEAD
            for k in range(20):
                experience = np.random.choice(training_data, p=p)
=======
            experience = exponentialWeightedChoice(training_data, 1)[0]
            experience = np.random.choice(training_data)
>>>>>>> master

                state0 = experience.state0
                state1 = experience.state1
                action = experience.action
                value = experience.value

                [actions0, actions1] = self.dqn_run([state0, state1])
                action = np.argmax(actions0)
                actions0[action] = (1 - discount) * value + discount * np.max(actions1)
                states0 = np.concatenate((states0, np.reshape(state0, (1, Model.state_size))), axis=0)
                expected = np.concatenate((expected, np.reshape(actions0, (1, self.action_size))), axis=0)

<<<<<<< HEAD
                for i in range(5):
                    states = [state0] * self.action_size
                    actions = np.zeros((self.action_size, self.action_size))
                    for j in range(self.action_size):
                        actions[j][j] = 1
                    states1, values = self.model_run(states, actions)
=======
            for i in range(50):
                states = [state0] * self.action_size
                actions = np.arange(self.action_size).reshape((self.action_size, 1))
                states1, values = self.model_run(states, actions)
>>>>>>> master

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