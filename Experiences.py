import pickle
import os.path
import numpy as np
import math

def getValue(temperature, target, target_delta):
    if math.fabs(temperature - target) > target_delta:
            return 0
    return (target_delta - math.fabs(temperature - target)) / target_delta

class Experience:
    def __init__(self, temperature, humidity, solenoid, timestamp, target, target_delta):
        self.temperature = temperature
        self.humidity = humidity
        self.solenoid = solenoid
        self.timestamp = timestamp
        self.target = target
        self.target_delta = target_delta

class TrainingExperience:
    def __init__(self, state0, state1, action, value):
        self.state0 = state0
        self.state1 = state1
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

    def get(self):
        result = []

        if len(self.experiences) == 0:
            return result

        experience0 = self.experiences[0]
        state1 = [0] * 2

        for experience1 in self.experiences:

            # state
            state0 = state1
            del state1[0]
            delta = math.floor((experience1.temperature - experience1.target) * 10)
            state1.append(delta)

            # action
            action = 1 if experience1.solenoid else 0

            # value
            value = getValue(experience1.temperature, experience1.target, experience1.target_delta)

            result.append(TrainingExperience(state0, state1, action, value))

        return result

    def getLast(self):
        foo = self.get()
        return foo[-1]
