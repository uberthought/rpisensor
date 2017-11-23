#!/usr/bin/python3

from network import DQN
from Experiences import Experiences

dqn = DQN(2, 2)
experiences = Experiences()

print('experiences ', len(experiences.get()))

for i in range(270):
    loss = dqn.train(experiences)

    print('loss', loss)

    dqn.save()
