import pickle
import os.path
import numpy as np
import math
import random
import threading

state_size = 3
action_size = 4

def normalize_temperature(temperature):
    # max = 30
    # min = 0
    # return (temperature - min) / (max - min)
    # return temperature - 22
    return (temperature - 15) / 100

def create_state(target, temperature, outside):
    return np.array([normalize_temperature(target), normalize_temperature(outside), temperature - target])


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
            saved = pickle.load(open("experiences.p", "rb"))
            self.states0 = saved.states0
            self.actions = saved.actions
            self.values = saved.values
            self.states1 = saved.states1

            self.temperatures = saved.temperatures
            self.humidities = saved.humidities
            self.powers = saved.powers
            self.targets = saved.targets
            self.outsides = saved.outsides
            self.timestamps = saved.timestamps
        else:
            self.reset()
            self.save()
        self.last_state = np.full(state_size, math.inf)

    def __str__(self):
        return object.__str__(self) + str(len(self.states0))

    def reset(self):
        self.states0 = np.array([], dtype=np.float).reshape(0, state_size)
        self.actions = np.array([], dtype=np.float).reshape(0, action_size)
        self.states1 = np.array([], dtype=np.float).reshape(0, state_size)
        self.values = np.array([], dtype=np.float).reshape(0, 1)

        self.temperatures = np.array([], dtype=np.float)
        self.humidities = np.array([], dtype=np.float)
        self.powers = np.array([], dtype=np.int)
        self.targets = np.array([], dtype=np.float)
        self.outsides = np.array([], dtype=np.float)
        self.timestamps = np.array([], dtype=np.str)

    def save(self):
        pickle.dump(self, open("experiences.p", "wb"))

    def append(self):
        if os.path.exists('experiences.p'):
            saved = pickle.load(open("experiences.p", "rb"))
            self.states0 = np.append(saved.states0, self.states0, axis=0)
            self.actions = np.append(saved.actions, self.actions, axis=0)
            self.values = np.append(saved.values, self.values, axis=0)
            self.states1 = np.append(saved.states1, self.states1, axis=0)

            self.temperatures = np.append(saved.temperatures, self.temperatures)
            self.humidities = np.append(saved.humidities, self.humidities)
            self.powers = np.append(saved.powers, self.powers)
            self.targets = np.append(saved.targets, self.targets)
            self.outsides = np.append(saved.outsides, self.outsides)
            self.timestamps = np.append(saved.timestamps, self.timestamps)
        pickle.dump(self, open("experiences.p", "wb"))

    def add(self, temperature, humidity, power, timestamp, target, outside):
        self.add2(temperature, humidity, power, timestamp, target, outside)
        self.save()

    def add2(self, temperature, humidity, power, timestamp, target, outside):

        state0 = self.last_state
        state1 = create_state(target, temperature, outside)
        action = np.zeros(action_size)
        action[power] = 1
        value = np.full(1, getValue(temperature, target, power))
        
        self.states0 = np.concatenate((self.states0, [state0]), axis=0)
        self.actions = np.concatenate((self.actions, [action]), axis=0)
        self.states1 = np.concatenate((self.states1, [state1]), axis=0)
        self.values = np.concatenate((self.values, [value]), axis=0)

        self.temperatures = np.concatenate((self.temperatures, [temperature]))
        self.humidities = np.concatenate((self.humidities, [humidity]))
        self.powers = np.concatenate((self.powers, [power]))
        self.targets = np.concatenate((self.targets, [target]))
        self.outsides = np.concatenate((self.outsides, [outside]))
        self.timestamps = np.concatenate((self.timestamps, [timestamp]))
        self.last_state = state1

    def get(self):

        states0 = np.array([], dtype=np.float).reshape(0, state_size)
        actions = np.array([], dtype=np.float).reshape(0, action_size)
        states1 = np.array([], dtype=np.float).reshape(0, state_size)
        values = np.array([], dtype=np.float).reshape(0, 1)
        timestamps = np.array([], dtype=np.str).reshape(0, 1)

        state1 = []
        for i in range(len(self.timestamps)):
            target = self.targets[i]
            outside = self.outsides[i]
            temperature = self.temperatures[i]
            power = self.powers[i]
            timestamp = self.timestamps[i]

            state0 = state1[:]
            state1 = create_state(target, temperature, outside)
            action = np.zeros(action_size)
            action[power] = 1
            value = np.full(1, getValue(temperature, target, power))

            if len(state0) == 0 or np.any(state0 == None):
                continue

            states0 = np.concatenate((states0, [state0]), axis=0)
            actions = np.concatenate((actions, [action]), axis=0)
            states1 = np.concatenate((states1, [state1]), axis=0)
            values = np.concatenate((values, [value]), axis=0)

        return states0, actions, values, states1

    def last(self):
        states0, actions, values, states1 = self.get()
        if len(states0) > 0:
            return states0[-1], actions[-1], values[-1][0], states1[-1]
        return None, None, None, None

    def denormalize_temperature(temperature):
        return temperature * 100 + 15

