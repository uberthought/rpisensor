#!/usr/bin/python3

import time
import numpy as np
import random
import math

from threading import Thread

from Sensor import Sensor
from Solenoid import Solenoid
from network import DQN
from Experiences import Experiences
from Settings import Settings
from WebServer import WebServer
from Communication import Communication

sensor = Sensor()
solenoid = Solenoid()
experiences = Experiences()
dqn = DQN(2, 2)

print('experiences ', len(experiences.get()))

target = Settings.getTargetC()
target_delta = Settings.getTargetDelta()
temperature, humidity, timestamp = sensor.gather()
experiences.add(temperature, humidity, solenoid.on, timestamp, target, target_delta)
experience = experiences.getLast()
state = experience.state0
action = 0

thread = Thread(target=WebServer.run)
thread.start()

lastCopied = time.time()

while True:

    runStart = time.time()

    if Settings.getOn():

        experience = experiences.getLast()
        state = experience.state0
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
        experiences.add(temperature, humidity, solenoid.isOn(), timestamp, target, target_delta)

        target = Settings.getTargetC()
        target_delta = Settings.getTargetDelta()

        print(temperature * 9 / 5 + 32, state, action, 'actions', actions, 'value', experience.value)

    else:
        temperature, humidity, timestamp = sensor.gather()
        print(temperature * 9 / 5 + 32)

    time.sleep(5 - time.time() + runStart)

    if (time.time() - lastCopied) > 60:
        lastCopied = time.time()
        Communication.sendExperiences()
