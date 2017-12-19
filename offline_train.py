#!/usr/bin/python3

from network import Model
from Experiences import Experiences

model = Model(3, 2)
experiences = Experiences()

print('experiences ', len(experiences.get()))

for i in range(5):
    state_loss = model.state_train(experiences, True)
    print('state', state_loss)
    value_loss = model.value_train(experiences, True)
    print('value', value_loss)
    dqn_loss = model.dqn_train(experiences, True)
    print('dqn', dqn_loss)
    model.save()