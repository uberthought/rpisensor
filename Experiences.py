import pickle
import os.path
import numpy as np
import math

from network import Model

class Experience:

    def __init__(self, temperature, humidity, power, timestamp, target):
        self.temperature = temperature
        self.humidity = humidity
        self.power = power
        self.timestamp = timestamp
        self.target = target

    def getValue(temperature, target):
        return 1 - math.fabs(temperature - target)

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

    def add(self, temperature, humidity, power, timestamp, target):
        experience = Experience(temperature, humidity, power, timestamp, target)
        self.experiences.append(experience)
        pickle.dump(self.experiences, open("experiences.p", "wb"))

    def add2(self, temperature, humidity, power, timestamp, target):
        experience = Experience(temperature, humidity, power, timestamp, target)
        self.experiences.append(experience)

    def get(self):
        result = []

        if len(self.experiences) < 2:
            return result

        experience0 = self.experiences[0]
        state1 = [0] * Model.state_size

        value1 = Experience.getValue(experience0.temperature, experience0.target)

        for experience1 in self.experiences:

            # state
            state0 = state1[:]
            del state1[0]
            state1.append(experience1.temperature - experience1.target)

            # action
            action = np.zeros(Model.action_size)
            action[experience1.power] = 1

            # value
            value1 = Experience.getValue(experience1.temperature, experience1.target)

            result.append(TrainingExperience(state0, state1, action, value1))

            
        return result

    def getLast(self):
        foo = self.get()
        if any(foo):
            return foo[-1]
        return None
