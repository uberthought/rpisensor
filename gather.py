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

print('experiences ', len(experiences.get()))

target = Settings.getTargetC()
state = []
actions = []
action = 0
experience = None

for i in range(100):
    
    action = np.random.choice(Model.action_size, 1)[0]

    # if temperature < target - 1:
    #     action = 1
    # elif temperature > target + 1:
    #     action = 0

    if action == 0:
        solenoid.switchOff()
    else:
        solenoid.switchOn()

    if action == 0:
        solenoid.switchOff()
    elif action == 1:
        solenoid.switchLow()
    else:
        solenoid.switchHigh()

    simulation.step()
    temperature, humidity, timestamp = sensor.gather()
    experiences.add(temperature, humidity, solenoid.power, timestamp, target)

    target = Settings.getTargetC()

    if i % 100 == 0:
        print(temperature * 9 / 5 + 32, state, action, experience.value)
    
