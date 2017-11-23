#!/usr/bin/python3

import datetime
import math
import random

class Simulation:
    def __init__(self):
        self.t = 0
        self.tdelta = 1
        self.temperature = 27 + (random.random() - 0.5) * 2
        self.humidity = 50
        self.on = False

    def step(self):
        self.t += self.tdelta
        timestamp = datetime.datetime(2017, 11, 20, 9, 28)
        timestamp += datetime.timedelta(minutes=self.t)

        if self.on:
            self.temperature += 20 / 60

        self.temperature -= 5 / 60

        return self.temperature, self.humidity, timestamp, self.getValue()

    def isOn(self):
        return self.on

    def getValue(self):
        return -math.pow(math.fabs(self.temperature - 27), 3)

    def switchOn(self):
        self.on = True

    def switchOff(self):
        self.on = False

