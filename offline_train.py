#!/usr/bin/python3

from network import Model
from Experiences import Experiences

model = Model(3, 2)
experiences = Experiences()

print('experiences ', len(experiences.get()))

for i in range(10):
    model_loss = model.model_train(experiences)
    print('model', model_loss)
    model.save()

for i in range(10):
    dqn_loss = model.dqn_train(experiences)
    print('dqn', dqn_loss)
    model.save()