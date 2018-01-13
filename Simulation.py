#!/usr/bin/python3

import pickle
import os.path
import datetime
import math
import random

from Settings import Settings

class Simulation:
    outside = 20
    
    def __init__(self):
        self.t = 0
        self.tdelta = 2
        # self.temperature = Settings.getTargetC() + (random.random() - 0.5) * 2
        self.temperature = Settings.getTargetC()
        self.humidity = 50
<<<<<<< HEAD
        self.power = 0
        self.insulation = 3
=======
        self.outside = 15
        self.low = False
        self.high = False
>>>>>>> master

    def init():
        if os.path.exists('simulation.p'):
            return pickle.load(open("simulation.p", "rb"))
        return Simulation()

    def step(self):
        self.t += self.tdelta

<<<<<<< HEAD
        if self.power == 1:
            self.temperature += 5 / 60
        elif self.power == 2:
            self.temperature += 20 / 60
        if self.power == 3:
            self.temperature -= 5 / 60

        self.temperature += ((Simulation.outside - self.temperature) / self.insulation) / 60
=======
        if self.low:
            self.temperature += 5 / 60
        if self.high:
            self.temperature += 10 / 60

        self.temperature = (self.temperature - self.outside) * math.exp(-0.008) + self.outside
>>>>>>> master

        pickle.dump(self, open("simulation.p", "wb"))


    def gather(self):
        timestamp = datetime.datetime.now()
<<<<<<< HEAD
        return self.temperature, 50, timestamp, Simulation.outside

    def setPower(self, power):
        self.power = power
=======
        return self.temperature, 50, timestamp

    def setLow(self):
        self.low = True
        self.high = False

    def setHigh(self):
        self.high = True
        self.low = False

    def setOff(self):
        self.high = False
        self.low = False
    
    def getState(self):
        if self.high:
            return 2
        elif self.low:
            return 1
        return 0
>>>>>>> master
