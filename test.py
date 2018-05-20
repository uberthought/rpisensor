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

temperature = target = Settings.getTargetC()
state0 = None
actions = []
action = 0
start = time.time()

while True:

    if random.random() < 0.2:
        state0 = None

    force=False
    explore=False

    if (temperature - target) < -1.0:
        action = 2
        force=True
    elif (temperature - target) > 1.0:
        action = 3
        force=True
    elif state0 is None:
        action = np.random.choice(Model.action_size, 1)[0]
        explore=True
    else:
        action = model.dqn_run_action([state0])

    solenoid.setPower(action)

    simulation.step()
    temperature, humidity, timestamp, outside = sensor.gather()
    experiences.add(temperature, humidity, solenoid.power, timestamp, target, outside)
    state0, _, value, _ = experiences.last()

    print('state0', state0)
    print('value', value)

    target = Settings.getTargetC()

    if force:
        action_type='f'
    elif explore:
        action_type='e'
    else:
        action_type=' '

    last = start
    start = time.time()
    if value != None:
        print("{0:0.2f}".format(temperature), str(action)+action_type, "{0:0.2f}".format(value), "{0:0.2f}".format(start-last), state0)
