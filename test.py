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
<<<<<<< HEAD
=======
temperature, humidity, timestamp = sensor.gather()
experiences.add(temperature, humidity, solenoid.on, timestamp, target)
experiences.add(temperature, humidity, solenoid.on, timestamp, target)
experience = None
>>>>>>> master
state = []
actions = []
action = 0
experience = None

while True:

    if experience is None:
<<<<<<< HEAD
        action = np.random.choice(Model.action_size, 1)[0]
    else:
=======
>>>>>>> master
        state = experience.state0
        action = model.dqn_run_action([state])

    solenoid.setPower(action)

    simulation.step()
    temperature, humidity, timestamp = sensor.gather()
<<<<<<< HEAD
    experiences.add(temperature, humidity, solenoid.power, timestamp, target)
=======

    experiences.add(temperature, humidity, solenoid.isOn(), timestamp, target)
>>>>>>> master
    experience = experiences.getLast()

    target = Settings.getTargetC()

    value = Experience.getValue(temperature, target, action)

    print(temperature, state, action, actions, value)
