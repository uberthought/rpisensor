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

temperature, humidity, timestamp, value = simulation.step()
isOn = simulation.isOn()
temperature_list = [temperature] * 2
state0 = list(temperature_list)
# state0.append(1 if isOn else 0)

for iteration in range(2700):

    # temperature, humidity, timestamp = sensor.gather()
    # isOn = solenoid.isOn()

    actions = dqn.run([state0])
    action = np.argmax(actions)

    if action == 0:
        simulation.switchOff()
    else:
        simulation.switchOn()

    temperature, humidity, timestamp, value = simulation.step()
    isOn = simulation.isOn()

    del temperature_list[0]
    temperature_list.append(temperature)

    state1 = list(temperature_list)
    # state1.append(1 if isOn else 0)
    experiences.add(state0, state1, action, value)
    state0 = state1

    print('states', state0, 'on', isOn, 'value', value)

    # time.sleep(5)
