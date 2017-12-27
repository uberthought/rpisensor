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
target_delta = Settings.getTargetDelta()
temperature, humidity, timestamp = sensor.gather()
experiences.add(temperature, humidity, solenoid.on, timestamp, target, target_delta)
experiences.add(temperature, humidity, solenoid.on, timestamp, target, target_delta)
experience = experiences.getLast()
state = []
actions = []
action = 0

while True:

    if experience.value != 0:
        state = experience.state0
        actions = model.dqn_run([state])
        action = np.argmax(actions)
        if random.random() < 0.05:
            action = abs(action - 1)
            # action = np.random.choice(2, 1)[0]

    if temperature < target - target_delta:
        action = 1
    elif temperature > target + target_delta:
        action = 0

    if action == 0:
        solenoid.switchOff()
    else:
        solenoid.switchOn()

    simulation.step()
    temperature, humidity, timestamp = sensor.gather()
    # if not force:
    experiences.add(temperature, humidity, solenoid.isOn(), timestamp, target, target_delta)
    experience = experiences.getLast()

    model_loss = model.model_train(experiences)
    dqn_loss = model.dqn_train(experiences)

    target = Settings.getTargetC()
    target_delta = Settings.getTargetDelta()
    model.save()

    value = Experience.getValue(temperature, target, target_delta)

    print(temperature * 9 / 5 + 32, state, action, actions, value)
