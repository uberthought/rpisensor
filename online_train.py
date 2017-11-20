#!/usr/bin/python3

from network import DQN
from Simulation import Simulation
from Experiences import Experiences

import numpy as np
import random

dqn = DQN(5, 2)

experiences = Experiences()
simulation = Simulation()

print('experiences ', len(experiences.get()))

iteration = 0
temperature, humidity, timestamp, value = simulation.step()
isOn = simulation.isOn()
temperature_list = [temperature] * 4
state0 = list(temperature_list)
state0.append(1 if isOn else 0)

for iteration in range(27):

    actions = dqn.run([state0])
    if random.random() < 0.25:
        action = np.random.choice(2, 1)[0]
    else:
        action = np.argmax(actions)

    temperature, humidity, timestamp, value = simulation.step()
    isOn = simulation.isOn()

    del temperature_list[0]
    temperature_list.append(temperature)

    state1 = list(temperature_list)
    state1.append(1 if isOn else 0)
    experiences.add(state0, state1, action, value)
    state0 = state1

    loss = dqn.train(experiences)
    print(loss)

dqn.save()