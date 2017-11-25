#!/usr/bin/python3

import time
import numpy as np
import math

from Sensor import Sensor
from Solenoid import Solenoid

from network import DQN
from Experiences import Experiences
from Settings import Settings

sensor = Sensor()
solenoid = Solenoid()
experiences = Experiences()
dqn = DQN(4, 2)

temperature, humidity, timestamp = sensor.gather()
experiences.add(temperature, humidity, solenoid.on, timestamp)
experience = experiences.getLast()
target = Settings.target
target_delta = Settings.target_delta
action = 0

while True:

    state = experience.state0
    # actions = dqn.run([state])
    # action = np.argmax(actions)

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
    print(temperature, action, timestamp)
    time.sleep(5)