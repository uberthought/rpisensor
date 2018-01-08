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

while True:

    if random.random() < 0.05:
        experience = None

    if (temperature - target) < -1.0:
        action = 2
    elif (temperature - target) > 1.0:
        action = 3
    elif experience is None:
        action = np.random.choice(Model.action_size, 1)[0]
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

    target = Settings.getTargetC()
    model.save()

    value = Experience.getValue(temperature, target, action)

    print(temperature, state, action, actions, value, model_loss, dqn_loss)
