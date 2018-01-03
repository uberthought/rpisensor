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
model = Model(3, 3)

print('experiences ', len(experiences.get()))

target = Settings.getTargetC()
experience = None
state = []
actions = []
action = 0

while True:

    if random.random() < 0.1:
        experience = None

    if experience is None:
        action = np.random.choice(3, 1)[0]
    else:
        state = experience.state0
        actions = model.dqn_run([state])
        action = np.argmax(actions)

    if action == 0:
        solenoid.setOff()
    elif action == 1:
        solenoid.setLow()
    else:
        solenoid.setHigh()

    simulation.step()
    temperature, humidity, timestamp = sensor.gather()
    experiences.add(temperature, humidity, solenoid.getState(), timestamp, target)
    experience = experiences.getLast()

    model_loss = model.model_train(experiences)
    dqn_loss = model.dqn_train(experiences)

    target = Settings.getTargetC()
    model.save()

    value = Experience.getValue(temperature, target)

    print(temperature * 9 / 5 + 32, state, action, actions, value, model_loss, dqn_loss)
