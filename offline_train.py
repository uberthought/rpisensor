#!/usr/bin/python3

from network import Model
from Experiences import Experiences
import numpy as np

model = Model()
experiences = Experiences()

print('experiences ', len(experiences.get()[0]))

for i in range(10):
    model_loss = model.model_train(experiences, False)
    print('model', model_loss)
    model.save()

for i in range(10):
    dqn_loss = model.dqn_train(experiences, False)
    print('dqn', dqn_loss)
    model.save()