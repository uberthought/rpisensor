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

temperature = target = Settings.getTargetC()
state = []
actions = []
action = 0
experience = None
start = time.time()

while True:

    if random.random() < 0.2:
        experience = None

    force=False
    explore=False

    if (temperature - target) < -1.0:
        action = 2
        force=True
    elif (temperature - target) > 1.0:
        action = 3
        force=True
    elif experience is None:
        action = np.random.choice(Model.action_size, 1)[0]
        explore=True
    else:
        state = experience.state0
        action = model.dqn_run_action([state])

    solenoid.setPower(action)

    simulation.step()
    temperature, humidity, timestamp, outside = sensor.gather()
    experiences.add(temperature, humidity, solenoid.power, timestamp, target, outside)
    experience = experiences.getLast()

    model_loss = model.model_train(experiences)
    dqn_loss = model.dqn_train(experiences)
    model.save()

    target = Settings.getTargetC()

    value = Experience.getValue(temperature, target, action)

    if force:
        action_type='f'
    elif explore:
        action_type='e'
    else:
        action_type=' '

    last = start
    start = time.time()
    print("{0:0.2f}".format(temperature), str(action)+action_type, "{0:0.2f}".format(value), "{0:0.2f}".format(start-last), state)
    # print ["{0:0.2f}".format(i) for i in a]

    # time.sleep(5)
