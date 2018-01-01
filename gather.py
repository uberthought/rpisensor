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

print('experiences ', len(experiences.get()))

target = Settings.getTargetC()
temperature, humidity, timestamp = sensor.gather()
experiences.add(temperature, humidity, solenoid.on, timestamp, target)
experiences.add(temperature, humidity, solenoid.on, timestamp, target)
experience = experiences.getLast()
action = 0

for i in range(100):
    
    experience = experiences.getLast()
    state = experience.state0
    if random.random() < 0.2:
        action = 0
    else:
        action = 1

    if temperature < target - 1:
        action = 1
    elif temperature > target + 1:
        action = 0

    if action == 0:
        solenoid.switchOff()
    else:
        solenoid.switchOn()

    simulation.step()

    temperature, humidity, timestamp = sensor.gather()
    experiences.add(temperature, humidity, solenoid.isOn(), timestamp, target)

    target = Settings.getTargetC()

    if i % 100 == 0:
        print(temperature * 9 / 5 + 32, state, action, experience.value)
    
