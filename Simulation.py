#!/usr/bin/python3

import datetime
import math
import random

class Simulation:
    target = 27
    
    def __init__(self):
        self.t = 0
        self.tdelta = 1
        self.temperature = Simulation.target + (random.random() - 0.5) * 2
        self.humidity = 50
        self.on = False

    def step(self):
        self.t += self.tdelta
        timestamp = datetime.datetime(2017, 11, 20, 9, 28)
        timestamp += datetime.timedelta(minutes=self.t)

        if self.on:
            self.temperature += 20 / 60

        self.temperature -= (math.pow(self.temperature, 7) / math.pow(32, 7) * 20) / 60

        delta = math.floor((self.temperature - Simulation.target) * 10)

        return delta, self.humidity, timestamp, self.getValue()

    def isOn(self):
        return self.on

    def getValue(self):
        return -math.pow(math.fabs(self.temperature - Simulation.target), 3)

    def switchOn(self):
        self.on = True

    def switchOff(self):
        self.on = False

