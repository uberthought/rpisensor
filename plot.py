#!/usr/bin/python3

# import matplotlib
# matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np

from network import Model
from Experiences import Experience, Experiences

model = Model(3, 2)
experiences = Experiences()

print('experiences ', len(experiences.experiences))

temperatures = [x.temperature for x in experiences.experiences]
min = experiences.experiences[-1].target - experiences.experiences[-1].target_delta
max = experiences.experiences[-1].target + experiences.experiences[-1].target_delta
target = experiences.experiences[-1].target
target_delta = experiences.experiences[-1].target_delta

experiences2 = Experiences()
experiences2.experiences = []
for temperature in np.arange(min, max, .005):
    experiences2.add2(temperature, .5, False, 0, target, target_delta)

# foo2 = experiences.get()
foo2 = experiences2.get()
actualValues2 = []
predictedValues2 = []
actions2 = []
temperatures2 = []
for experience in foo2:
    states1, values = model.model_run([experience.state1], [[experience.value]])

    actions = model.dqn_run([experience.state0])
    action = actions[0]
    action = np.append(action, np.argmax(actions))

    temperatures2.append(experience.state1[2])
    predictedValues2.append(values[0][0])
    actualValues2.append(experience.value)
    actions2.append(action)

temperatures2 = temperatures2[2:]
actualValues2 = actualValues2[2:]
predictedValues2 = predictedValues2[2:]
actions2 = actions2[2:]

# actions2 = actions2 / np.max(actions2, axis=0)

fig, ax = plt.subplots()
ax.plot(temperatures2, [x[0] for x in actions2], label='off')
ax.plot(temperatures2, [x[1] for x in actions2], label='on')
ax.plot(temperatures2, [x[2] for x in actions2], label='trigger')
ax.plot(temperatures2, actualValues2, label='actual value')
ax.plot(temperatures2, predictedValues2, label='predicted value')

legend = ax.legend(loc='lower right')
for label in legend.get_lines():
    label.set_linewidth(2)
for label in legend.get_texts():
    label.set_fontsize('large')

plt.savefig("plot.png")
plt.show()