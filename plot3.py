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
# min = experiences.experiences[-1].target - experiences.experiences[-1].target_delta
# max = experiences.experiences[-1].target + experiences.experiences[-1].target_delta
min = np.min(temperatures)
max = np.max(temperatures)
target = experiences.experiences[-1].target
target_delta = experiences.experiences[-1].target_delta

experiencesFake = Experiences()
experiencesFake.experiences = []
for temperature in np.arange(min, max, .01):
        experiencesFake.add2(temperature, .5, True, 0, target, target_delta)
        experiencesFake.add2(temperature, .5, False, 0, target, target_delta)

# fooFake = experiencesFake.get()[2:]
fooFake = experiences.get()
valuesOn = []
valuesOff = []
predictedOn = []
predictedOff = []
valuesDiff = []
temperaturesOn = []
temperaturesOff = []

for experience in fooFake:
    state0 = experience.state0
    state1 = experience.state1
    value = experience.value
    action = experience.action

    states0 = [state0, state0]
    actions = [[0], [1]]
    states1, values = model.model_run(states0, actions)

    if experience.action[0] == 0:
        temperaturesOff.append(state0[2])
        predictedOff.append(values[0][0])
        valuesOff.append(value)
        # valuesOff.append(values[0][0] - value)
        # statesDiff.append(experience.state1[2] - states1[0][2])
    else:
        temperaturesOn.append(state0[2])
        predictedOn.append(values[1][0])
        valuesOn.append(value)
        # valuesOn.append(values[1][0] - value)
        # statesDiff.append(experience.state1[2] - states1[1][2])
    

# valuesDiff = np.array(valuesDiff) * 10

fig, ax = plt.subplots(figsize=(20, 10))
# fig, ax = plt.subplots()
ax.plot(temperaturesOn, valuesOn, '.', label='actual on', color='red')
ax.plot(temperaturesOff, valuesOff, '.', label='actual off', color='blue')
ax.plot(temperaturesOn, predictedOn, '.', label='predicted on', color='gray')
ax.plot(temperaturesOff, predictedOff, '.', label='predicted off', color='green')
# ax.plot(temperatures, valuesOn, '.', label='on', color='red')
# ax.plot(temperatures, valuesOff, '.', label='off', color='blue')
# ax.plot(temperatures, valuesDiff, '.', label='on vs. off', color='gray')
# ax.plot(temperatures, values2, '.', label='values', color='green')
# ax.plot(temperatures, statesDiff, '.', label='values', color='green')

legend = ax.legend(loc='lower right')
for label in legend.get_lines():
    label.set_linewidth(2)
for label in legend.get_texts():
    label.set_fontsize('large')

plt.savefig("plot.png")
plt.show()