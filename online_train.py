#!/usr/bin/python3

from network import DQN
from Sensor import Sensor
from Solenoid import Solenoid
from Experiences import Experiences
from Settings import Settings

import time
import numpy as np
import random
import math

sensor = Sensor()
solenoid = Solenoid()
experiences = Experiences()
dqn = DQN(2, 2)

print('experiences ', len(experiences.get()))

temperature, humidity, timestamp = sensor.gather()
target = Settings.target
target_delta = Settings.target_delta
experiences.add(temperature, humidity, solenoid.on, timestamp)
experience = experiences.getLast()
state = experience.state0
action = 0

for iteration in range(270):

    actions = dqn.run([state])
    if random.random() < 0.5:
        action = np.random.choice(2, 1)[0]
    else:
        action = np.argmax(actions)

    if temperature < target - target_delta:
        action = 1
    elif temperature > target + target_delta:
        action = 0

    if action == 0:
        solenoid.switchOff()
    else:
        solenoid.switchOn()

    temperature, humidity, timestamp = sensor.gather()
    experiences.add(temperature, humidity, solenoid.on, timestamp)
    experience = experiences.getLast()
    state = experience.state0

    loss = dqn.train(experiences)
    print(temperature, state, action, 'actions', actions, 'value', experience.value, 'loss', loss)

    dqn.save()
    time.sleep(5)
