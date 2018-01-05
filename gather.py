#!/usr/bin/python3

from Simulation import Simulation
# from Sensor import Sensor
# from Solenoid import Solenoid
from network import Model
from Experiences import Experiences
from Settings import Settings

import time
import numpy as np
import random
import math

sensor = solenoid = simulation = Simulation.init()
# sensor = Sensor()
# solenoid = Solenoid()
experiences = Experiences()
model = Model()

target = Settings.getTargetC()
state = []
actions = []
action = 0

for j in range(10):
    simulation.temperature = target
    experiences.resetId()

    for i in range(100):
        
        action = np.random.choice(Model.action_size, 1)[0]

        solenoid.setPower(action)

        simulation.step()
        temperature, humidity, timestamp = sensor.gather()
        experiences.add(temperature, humidity, solenoid.power, timestamp, target)

        target = Settings.getTargetC()

    print(temperature, state, action)
        
