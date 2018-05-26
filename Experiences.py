import pickle
import os.path
import numpy as np
import math
import random
import threading

state_size = 4
action_size = 4

def normalize_temperature(temperature):
    # max = 30
    # min = 0
    # return (temperature - min) / (max - min)
    # return temperature - 22
    return (temperature - 15) / 100

def getValue(temperature, target, power):
    value = 1 - math.fabs(temperature - target)
    if power == 3:
        value -= 0.05
    if power == 2:
        value -= 0.3
    if power == 1:
        value -= 0.05
    return value

class Experiences:
    def __init__(self):
        if os.path.exists('experiences.p'):
            [self.states0, self.actions, self.values, self.states1, self.timestamps] = pickle.load(open("experiences.p", "rb"))
        else:
            self.reset()
        self.last_state = np.full(state_size, math.inf)

    def __str__(self):
        return object.__str__(self) + str(len(self.states0))

    def reset(self):
        self.states0 = np.array([], dtype=np.float).reshape(0, state_size)
        self.actions = np.array([], dtype=np.float).reshape(0, action_size)
        self.states1 = np.array([], dtype=np.float).reshape(0, state_size)
        self.values = np.array([], dtype=np.float).reshape(0, 1)
        self.timestamps = np.array([], dtype=np.str).reshape(0, 1)
        self.save()

    def save(self):
        pickle.dump([self.states0, self.actions, self.values, self.states1, self.timestamps], open("experiences.p", "wb"))

    def append(self):
        states0 = self.states0
        actions = self.actions
        values = self.values
        states1 = self.states1
        timestamps = self.timestamps
        if os.path.exists('experiences.p'):
            saved = pickle.load(open("experiences.p", "rb"))
            states0 = np.append(saved[0], states0, axis=0)
            actions = np.append(saved[1], actions, axis=0)
            values = np.append(saved[2], values, axis=0)
            states1 = np.append(saved[3], states1, axis=0)
            timestamps = np.append(saved[4], timestamps, axis=0)
        pickle.dump([states0, actions, values, states1, timestamps], open("experiences.p", "wb"))

    def add(self, temperature, humidity, power, timestamp, target, outside):
        self.add2(temperature, humidity, power, timestamp, target, outside)
        self.save()

    def add2(self, temperature, humidity, power, timestamp, target, outside):
        state0 = self.last_state
        state1 = np.array([normalize_temperature(target), normalize_temperature(outside), state0[3], temperature - target])
        action = np.zeros(action_size)
        action[power] = 1
        value = np.full(1, getValue(temperature, target, power))
        timestamp = np.full(1, timestamp)
        
        self.states0 = np.concatenate((self.states0, [state0]), axis=0)
        self.actions = np.concatenate((self.actions, [action]), axis=0)
        self.states1 = np.concatenate((self.states1, [state1]), axis=0)
        self.values = np.concatenate((self.values, [value]), axis=0)
        self.timestamps = np.concatenate((self.timestamps, [timestamp]), axis=0)
        self.last_state = state1

    def get(self):

        states0 = np.array([], dtype=np.float).reshape(0, state_size)
        actions = np.array([], dtype=np.float).reshape(0, action_size)
        states1 = np.array([], dtype=np.float).reshape(0, state_size)
        values = np.array([], dtype=np.float).reshape(0, 1)
        timestamps = np.array([], dtype=np.str).reshape(0, 1)

        for i in range(len(self.states0)):
            state0 = self.states0[i]
            state1 = self.states1[i]
            action = self.actions[i]
            value = self.values[i]
            timestamp = self.timestamps[i]
            if np.any(state0 == math.inf) or np.any(state1 == math.inf):
                continue
            if np.any(action == math.inf) or np.any(value == math.inf):
                continue
            states0 = np.concatenate((states0, [state0]), axis=0)
            actions = np.concatenate((actions, [action]), axis=0)
            states1 = np.concatenate((states1, [state1]), axis=0)
            values = np.concatenate((values, [value]), axis=0)
            timestamps = np.concatenate((timestamps, [timestamp]), axis=0)
            
        return states0, actions, values, states1, timestamps

    def last(self):
        state0, action, value, state1, timestamp = self.get()
        if len(state0) > 0:
            return state0[-1], action[-1], value[-1][0], state1[-1], timestamp[-1]
        return None, None, None, None, None

    def denormalize_temperature(temperature):
        return temperature * 100 + 15

