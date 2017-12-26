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
        experiencesFake.add2(temperature, .5, False, 0, target, target_delta)

fooFake = experiencesFake.get()[2:]
valuesOn = []
valuesOff = []
valuesDiff = []
temperatures = []

for experience in fooFake:
    state0 = experience.state0
    _, values = model.model_run([state0, state0], [[0], [1]])

    valuesOff.append(values[0][0])
    valuesOn.append(values[1][0])
    valuesDiff.append(values[1][0] - values[0][0])
    temperatures.append(experience.state0[2])

valuesOff = np.array(valuesOff) / 100
valuesOn = np.array(valuesOn) / 100

fig, ax = plt.subplots(figsize=(20, 10))
# fig, ax = plt.subplots()
ax.plot(temperatures, valuesOn, '.', label='on', color='red')
ax.plot(temperatures, valuesOff, '.', label='off', color='blue')
ax.plot(temperatures, valuesDiff, '.', label='diff', color='gray')

legend = ax.legend(loc='lower right')
for label in legend.get_lines():
    label.set_linewidth(2)
for label in legend.get_texts():
    label.set_fontsize('large')

plt.savefig("plot.png")
plt.show()