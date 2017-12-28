#!/usr/bin/python3

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np

from network import Model
from Experiences import Experience, Experiences

model = Model(3, 2)
experiences = Experiences()

print('experiences ', len(experiences.experiences))

# temperatures = [x.temperature for x in experiences.experiences]
# min = np.min(temperatures)
# max = np.max(temperatures)
min = experiences.experiences[-1].target - experiences.experiences[-1].target_delta
max = experiences.experiences[-1].target + experiences.experiences[-1].target_delta
target = experiences.experiences[-1].target
target_delta = experiences.experiences[-1].target_delta

experiencesFake = Experiences()
experiencesFake.experiences = []
for temperature in np.arange(min, max, .01):
    experiencesFake.add2(temperature, .5, False, 0, target, target_delta)

fooFake = experiencesFake.get()[2:]
predictedOn = []
predictedOff = []
temperatures = []

for experience in fooFake:
    state0 = experience.state0

    states0 = [state0, state0]
    actions = [[0], [1]]
    states1, values = model.model_run(states0, actions)

    temperatures.append(state0[2])
    predictedOff.append(values[0][0])
    predictedOn.append(values[1][0])

fooFake = experiences.get()
valuesOn = []
valuesOff = []
temperaturesOn = []
temperaturesOff = []

for experience in fooFake:
    state0 = experience.state0
    value = experience.value

    if experience.action[0] == 0:
        temperaturesOff.append(state0[2])
        valuesOff.append(value)
    else:
        temperaturesOn.append(state0[2])
        valuesOn.append(value)


fig, ax = plt.subplots(figsize=(20, 10))
ax.plot(temperatures, predictedOn, label='predicted on', color='red')
ax.plot(temperatures, predictedOff, label='predicted off', color='blue')
ax.plot(temperaturesOn, valuesOn, 'o', label='actual on', color='red')
ax.plot(temperaturesOff, valuesOff, 'o', label='actual off', color='blue')

legend = ax.legend(loc='lower right')
for label in legend.get_lines():
    label.set_linewidth(2)
for label in legend.get_texts():
    label.set_fontsize('large')

plt.savefig("plotValue.png")
plt.show()
