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

temperature, humidity, timestamp, value = simulation.step()
temperature_list = [temperature] * 2
state0 = list(temperature_list)
iterations = 0

while temperature >= -30 and temperature <= 30:
    iterations += 1

    # temperature, humidity, timestamp = sensor.gather()

    actions = dqn.run([state0])
    action = np.argmax(actions)

    if action == 0:
        simulation.switchOff()
    else:
        simulation.switchOn()

    temperature, humidity, timestamp, value = simulation.step()

    del temperature_list[0]
    temperature_list.append(temperature)

    state0 = list(temperature_list)

    print(state0, action, 'actions', actions, 'value', value)

    # time.sleep(5)
print(iterations)