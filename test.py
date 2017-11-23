#!/usr/bin/python3

# import os.path
import time
# import datetime
import numpy as np
import math

# from Sensor import Sensor
# from Solenoid import Solenoid

from network import DQN
from Simulation import Simulation

# sensor = Sensor()
# solenoid = Solenoid()
simulation = Simulation()
dqn = DQN(2, 2)

delta, humidity, timestamp, value = simulation.step()
state_list = [delta] * 2
state0 = list(state_list)
iterations = 0

while simulation.temperature >= 24 and simulation.temperature <= 30:
    iterations += 1

    # delta, humidity, timestamp = sensor.gather()

    actions = dqn.run([state0])
    action = np.argmax(actions)

    if action == 0:
        simulation.switchOff()
    else:
        simulation.switchOn()

    delta, humidity, timestamp, value = simulation.step()

    del state_list[0]
    state_list.append(delta)

    state0 = list(state_list)

    print(simulation.temperature, state0, action, 'actions', actions, 'value', value)

    # time.sleep(5)
print(iterations)