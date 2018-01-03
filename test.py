#!/usr/bin/python3

from Simulation import Simulation
# from Sensor import Sensor
# from Solenoid import Solenoid
from network import Model
from Experiences import Experience, Experiences
from Settings import Settings

import time
import numpy as np
import random
import math

sensor = solenoid = simulation = Simulation.init()
# sensor = Sensor()
# solenoid = Solenoid()
experiences = Experiences()
model = Model(3, 2)

print('experiences ', len(experiences.get()))

target = Settings.getTargetC()
temperature, humidity, timestamp = sensor.gather()
experiences.add(temperature, humidity, solenoid.on, timestamp, target)
experiences.add(temperature, humidity, solenoid.on, timestamp, target)
experience = None
state = []
actions = []
action = 0

while True:

    if experience is None:
        state = experience.state0
        actions = model.dqn_run([state])
        action = np.argmax(actions)

    if action == 0:
        solenoid.switchOff()
    else:
        solenoid.switchOn()

    simulation.step()
    temperature, humidity, timestamp = sensor.gather()

    experiences.add(temperature, humidity, solenoid.isOn(), timestamp, target)
    experience = experiences.getLast()

    target = Settings.getTargetC()

    value = Experience.getValue(temperature, target)

    print(temperature * 9 / 5 + 32, state, action, actions, value)
