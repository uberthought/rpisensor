import pickle
import os.path
import numpy as np
import math

from Settings import Settings

class Experience:
    def __init__(self, temperature, humidity, solenoid, timestamp):
        self.temperature = temperature
        self.humidity = humidity
        self.solenoid = solenoid
        self.timestamp = timestamp

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

    def add(self, temperature, humidity, solenoid, timestamp):
        experience = Experience(temperature, humidity, solenoid, timestamp)
        self.experiences.append(experience)
        pickle.dump(self.experiences, open("experiences.p", "wb"))

    def get(self):
        result = []

        if len(self.experiences) == 0:
            return result

        experience0 = self.experiences[0]
        state1 = [0] * 2
        target = Settings.target
        target_delta = Settings.target_delta

        for experience1 in self.experiences:

            # state
            state0 = state1
            del state1[0]
            delta = math.floor((experience1.temperature - target) * 10)
            state1.append(delta)

            # action
            action = 1 if experience1.solenoid else 0

            # value
            if math.fabs(experience1.temperature - target) > target_delta:
                    value = 0
            else:
                value = (target_delta - math.fabs(experience1.temperature - target)) / target_delta

            result.append(TrainingExperience(state0, state1, action, value))

        return result

    def getLast(self):
        foo = self.get()
        return foo[-1]
