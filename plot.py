#!/usr/bin/python3

# import matplotlib
# matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np

from network import Model
from Experiences import Experiences

model = Model(3, 2)
experiences = Experiences()

foo = experiences.experiences
print('experiences ', len(foo))

temperatures = [x.temperature for x in foo]
max = np.max(temperatures)
min = np.min(temperatures)

experiences2 = Experiences()
experiences2.experiences = []
for temperature in np.arange(min, max, .005):
    experiences2.add2(temperature, .5, False, 0, 24, 0.5)

foo2 = experiences2.get()
actualValues2 = []
predictedValues2 = []
temperatures2 = []
actions2 = []
state_rms2 = []
value_rms2 = []
for experience in foo2:
    state0 = experience.state0
    action = experience.action
    states1, values = model.model_run([state0], [action])
    state1 = states1[0]
    state_diff = state1 - experience.state1
    value_diff = values[0][0] - experience.value
    state_rms = np.sqrt(np.mean(state_diff**2))
    value_rms = np.sqrt(np.mean(value_diff**2))
    actions = model.dqn_run([state0])
    action = actions[0]
    action = np.append(action, np.argmax(actions))

    temperatures2.append(experience.state0[1])
    actualValues2.append(values[0][0])
    predictedValues2.append(experience.value)
    actions2.append(action)
    state_rms2.append(state_rms)
    value_rms2.append(value_rms)


temperatures2 = temperatures2[2:]
actions2 = actions2[2:]
actualValues2 = actualValues2[2:]
predictedValues2 = predictedValues2[2:]
state_rms2 = state_rms2[2:]
value_rms2 = value_rms2[2:]

fig, ax = plt.subplots()
# ax.plot(temperatures2, [x[0] for x in actions2], label='off')
# ax.plot(temperatures2, [x[1] for x in actions2], label='on')
# ax.plot(temperatures2, [x[2] for x in actions2], label='trigger')
ax.plot(temperatures2, actualValues2, label='actual value')
ax.plot(temperatures2, predictedValues2, label='predicted value')
# ax.plot(temperatures2, state_rms2, label='state error')
ax.plot(temperatures2, value_rms2, label='value error')

legend = ax.legend(loc='upper right')
for label in legend.get_lines():
    label.set_linewidth(2)
for label in legend.get_texts():
    label.set_fontsize('large')

plt.savefig("plot.png")
plt.show()

# for i in range(270):
#     model_loss = model.model_train(experiences)
#     dqn_loss = model.dqn_train(experiences)
#     print('model', model_loss, 'dqn', dqn_loss)
#     model.save()