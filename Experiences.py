import pickle
import os.path
import numpy as np
import math

class Experience:

    def __init__(self, temperature, humidity, solenoid, timestamp, target):
        self.temperature = temperature
        self.humidity = humidity
        self.solenoid = solenoid
        self.timestamp = timestamp
        self.target = target

    def getValue(temperature, target):
        return 1 - math.fabs(temperature - target)

class TrainingExperience:
    def __init__(self, state0, state1, action, value):
        self.state0 = state0[:]
        self.state1 = state1[:]
        self.action = action
        self.value = value

class Experiences:
    def __init__(self):
        self.experiences = []
        if os.path.exists('experiences.p'):
            self.experiences = pickle.load(open("experiences.p", "rb"))

    def add(self, temperature, humidity, solenoid, timestamp, target):
        experience = Experience(temperature, humidity, solenoid, timestamp, target)
        self.experiences.append(experience)
        pickle.dump(self.experiences, open("experiences.p", "wb"))

    def add2(self, temperature, humidity, solenoid, timestamp, target):
        experience = Experience(temperature, humidity, solenoid, timestamp, target)
        self.experiences.append(experience)

    def stateToTemperature(self, state):
        return state[2]

    def get(self):
        result = []

        if len(self.experiences) < 2:
            return result

        experience0 = self.experiences[0]
        state1 = [experience0.temperature] * 3
        state1[0] = experience0.target

        value1 = Experience.getValue(experience0.temperature, experience0.target)

        for experience1 in self.experiences:

            # state
            state0 = state1[:]
            del state1[1]
            state1.append(experience1.temperature)
            state1[0] = experience1.target

            # action
            action = [1 if experience1.solenoid else 0]

            # value
            value1 = Experience.getValue(experience1.temperature, experience1.target)
            result.append(TrainingExperience(state0, state1, action, value1))

        return result

    def getLast(self):
        foo = self.get()
        if any(foo):
            return foo[-1]
        return TrainingExperience([], [], 0, 0)
