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
model = Model()

target = Settings.getTargetC()
state = []
actions = []
action = 0
experience = None

while True:

    if experience is None:
        action = np.random.choice(Model.action_size, 1)[0]
    else:
        state = experience.state0
        actions = model.dqn_run([state])
        action = np.argmax(actions)

    solenoid.setPower(action)

    simulation.step()
    temperature, humidity, timestamp = sensor.gather()
    experiences.add(temperature, humidity, solenoid.power, timestamp, target)
    experience = experiences.getLast()

    target = Settings.getTargetC()

    value = Experience.getValue(temperature, target, action)

    print(temperature, state, action, actions, value)
