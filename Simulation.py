#!/usr/bin/python3

import pickle
import os.path
import datetime
import math
import random

from Settings import Settings

class Simulation:
    
    def __init__(self):
        self.t = 0
        self.tdelta = 2
        # self.temperature = Settings.getTargetC() + (random.random() - 0.5) * 2
        self.temperature = Settings.getTargetC()
        self.humidity = 50
        self.power = 0

    def init():
        if os.path.exists('simulation.p'):
            return pickle.load(open("simulation.p", "rb"))
        return Simulation()

    def step(self):
        self.t += self.tdelta

        if self.power == 1:
            self.temperature += 4 / 60
        elif self.power == 2:
            self.temperature += 20 / 60
        if self.power == 3:
            self.temperature -= 3 / 60

        self.temperature -= (math.pow(self.temperature, 7) / math.pow(30, 7) * 30) / 60

        pickle.dump(self, open("simulation.p", "wb"))


    def gather(self):
        timestamp = datetime.datetime.now()
        return self.temperature, 50, timestamp

    def setPower(self, power):
        self.power = power
