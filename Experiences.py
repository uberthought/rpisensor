import pickle
import os.path
import numpy as np
import math

class Experience:
    minTemperature = 23
    maxTemperature = 25

    def __init__(self, temperature, humidity, solenoid, timestamp, target, target_delta):
        self.temperature = temperature
        self.humidity = humidity
        self.solenoid = solenoid
        self.timestamp = timestamp
        self.target = target
        self.target_delta = target_delta

    def getValue(temperature, target, target_delta):
        result = (target_delta - math.fabs(temperature - target)) / target_delta
        result = result * 9
        return result

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

    def add(self, temperature, humidity, solenoid, timestamp, target, target_delta):
        experience = Experience(temperature, humidity, solenoid, timestamp, target, target_delta)
        self.experiences.append(experience)
        pickle.dump(self.experiences, open("experiences.p", "wb"))

    def add2(self, temperature, humidity, solenoid, timestamp, target, target_delta):
        experience = Experience(temperature, humidity, solenoid, timestamp, target, target_delta)
        self.experiences.append(experience)

    def get(self):
        result = []

        if len(self.experiences) < 2:
            return result

        experience0 = self.experiences[0]
        state1 = [0] * 3

        min = Experience.minTemperature
        max = Experience.maxTemperature

        state1[0] = (experience0.target - min) / (max - min)

        value1 = Experience.getValue(experience0.temperature, experience0.target, experience0.target_delta)

        for experience1 in self.experiences:

            # state
            state0 = state1[:]
            del state1[0]
            foo = (experience1.temperature - experience1.target) / (max - min)
            state1.append(foo)

            # action
            action = [1 if experience1.solenoid else 0]

            # value
            value0 = value1
            value1 = Experience.getValue(experience1.temperature, experience1.target, experience1.target_delta)
            value = value1 - value0

            if value != 0:
                result.append(TrainingExperience(state0, state1, action, value))

        return result

    def getLast(self):
        foo = self.get()
        if any(foo):
            return foo[-1]
        return TrainingExperience([], [], 0, 0)
