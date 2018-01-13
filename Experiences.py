import pickle
import os.path
import numpy as np
import math
import random

from network import Model

def normalize_temperature(temperature):
    max = 30
    min = 0
    return (temperature - min) / (max - min)

class Experience:

    def __init__(self, temperature, humidity, power, timestamp, target, outside, id):
        self.temperature = temperature
        self.humidity = humidity
        self.power = power
        self.timestamp = timestamp
        self.target = target
        self.outside = outside
        self.id = id

    def getValue(temperature, target, power):
        value = 1 - math.fabs(temperature - target)
        if power == 3:
            value -= 0.05
        if power == 2:
            value -= 0.3
        if power == 1:
            value -= 0.05
        return value

class TrainingExperience:
    def __init__(self, state0, state1, action, value):
        self.state0 = state0[:]
        self.state1 = state1[:]
        self.action = action[:]
        self.value = value

class Experiences:
    def __init__(self):
        self.experiences = []
        if os.path.exists('experiences.p'):
            self.experiences = pickle.load(open("experiences.p", "rb"))
        self.id = random.random()

    def add(self, temperature, humidity, power, timestamp, target, outside):
        experience = Experience(temperature, humidity, power, timestamp, target, outside, self.id)
        self.experiences.append(experience)
        pickle.dump(self.experiences, open("experiences.p", "wb"))

    def add2(self, temperature, humidity, power, timestamp, target, outside):
        experience = Experience(temperature, humidity, power, timestamp, target, outside, self.id)
        self.experiences.append(experience)

    def resetId(self):
        self.id = random.random()

    def get(self):
        if len(self.experiences) < 2:
            return None

        result = []

        experience0 = self.experiences[0]
        state1 = [experience0.temperature - experience0.target] * Model.state_size
        state1[0] = normalize_temperature(experience0.target)
        state1[1] = normalize_temperature(experience0.outside)

        value1 = Experience.getValue(experience0.temperature, experience0.target, experience0.power)

        for experience1 in self.experiences:

            if experience0.id == experience1.id:
                # state
                state0 = state1[:]
                del state1[2]
                state1.append(experience1.temperature - experience1.target)
                state1[0] = normalize_temperature(experience1.target)
                state1[1] = normalize_temperature(experience1.outside)

                # action
                action = np.zeros(Model.action_size)
                action[experience1.power] = 1

                # value
                value1 = Experience.getValue(experience1.temperature, experience1.target, experience1.power)

                result.append(TrainingExperience(state0, state1, action, value1))
            else:
                state1 = [experience1.temperature - experience1.target] * Model.state_size
                state0 = state1[:]

            experience0 = experience1

            
        return result

    def getLast(self):
        foo = self.get()
        if foo is not None:
            return foo[-1]
        return None
