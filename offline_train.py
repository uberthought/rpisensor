#!/usr/bin/python3

from pendulum import Pendulum
from network import DQN

import pickle
import os.path

dqn = DQN(Pendulum.state_size, Pendulum.action_size)

if os.path.exists('experiences.p'):
    experiences = pickle.load(open("experiences.p", "rb"))
print('experiences ', len(experiences))

for i in range(270):
    loss = dqn.train(experiences)

    print('loss', loss)

    dqn.save()
