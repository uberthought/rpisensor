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
        self.tdelta = 1
        self.temperature = Settings.getTargetC() + (random.random() - 0.5) * 2
        self.humidity = 50
        self.on = False

    def init():
        if os.path.exists('simulation.p'):
            return pickle.load(open("simulation.p", "rb"))
        return Simulation()

    def step(self):
        self.t += self.tdelta

        if self.on:
            self.temperature += 20 / 60

        self.temperature -= (math.pow(self.temperature, 7) / math.pow(30, 7) * 20) / 60

        pickle.dump(self, open("simulation.p", "wb"))


    def gather(self):
        timestamp = datetime.datetime.now()
        return self.temperature, 50, timestamp

    def switchOn(self):
        self.on = True

    def switchOff(self):
        self.on = False

    def isOn(self):
        return self.on

