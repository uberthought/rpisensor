#!/usr/bin/python3

# import os.path
import time
# import datetime
import numpy as np

# from Sensor import Sensor
# from Solenoid import Solenoid

from network import DQN
from Simulation import Simulation
from Experiences import Experiences

# sensor = Sensor()
# solenoid = Solenoid()
experiences = Experiences()
simulation = Simulation()
dqn = DQN(2, 2)

print('experiences ', len(experiences.get()))

delta, humidity, timestamp, value = simulation.step()
state_list = [delta] * 2
state0 = list(state_list)

for iteration in range(2700):

    # delta, humidity, timestamp = sensor.gather()
35.202.235.6
    actions = dqn.run([state0])
    action = np.argmax(actions)

    if simulation.temperature < 26:
        action = 1
    else if simulation.temperature > 28:
        action = 0

    if action == 0:
        simulation.switchOff()
    else:
        simulation.switchOn()

    delta, humidity, timestamp, value = simulation.step()

    del state_list[0]
    state_list.append(delta)

    state1 = list(state_list)
    experiences.add(state0, state1, action, value)
    state0 = state1

    print(state0, action, 'actions', actions, 'value', value)

    if simulation.temperature < -24 or simulation.temperature > 30:
        simulation = Simulation()
        delta, humidity, timestamp, value = simulation.step()
        state_list = [delta] * 2
        state0 = list(state_list)


    # time.sleep(5)
