#!/usr/bin/python3

# import matplotlib
# matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np

from network import Model
from Experiences import Experience, Experiences

model = Model(3, 3)
experiences = Experiences()

print('experiences ', len(experiences.experiences))

target = experiences.experiences[-1].target
temperatures = [x.temperature for x in experiences.experiences]
min = np.min(temperatures)
max = np.max(temperatures)

experiencesFake = Experiences()
experiencesFake.experiences = []
for temperature in np.arange(min, max, .01):
    experiencesFake.add2(temperature, .5, False, 0, target)

fooFake = experiencesFake.get()[2:]
predictedOff = []
predictedLow = []
predictedHigh = []
temperatures = []

for experience in fooFake:
    state0 = experience.state0

    states0 = [state0] * 3
    actions = np.arange(3).reshape((3, 1))
    states1, values = model.model_run(states0, actions)

    temperatures.append(experiences.stateToTemperature(experience.state0))
    predictedOff.append(values[0][0])
    predictedLow.append(values[1][0])
    predictedHigh.append(values[2][0])

fooFake = experiences.get()
valuesOff = []
temperaturesOff = []
valuesLow = []
temperaturesLow = []
valuesHigh = []
temperaturesHigh = []

for experience in fooFake:
    state0 = experience.state0
    value = experience.value

    if experience.action == 0:
        temperaturesOff.append(experiences.stateToTemperature(state0))
        valuesOff.append(value)
    elif experience.action == 1:
        temperaturesLow.append(experiences.stateToTemperature(state0))
        valuesLow.append(value)
    else:
        temperaturesHigh.append(experiences.stateToTemperature(state0))
        valuesHigh.append(value)


fig, ax = plt.subplots(figsize=(20, 10))
ax.plot(temperatures, predictedOff, label='predicted off', color='blue')
ax.plot(temperatures, predictedLow, label='predicted low', color='green')
ax.plot(temperatures, predictedHigh, label='predicted high', color='red')
ax.plot(temperaturesOff, valuesOff, 'o', label='actual on', color='blue')
ax.plot(temperaturesLow, valuesLow, 'o', label='actual off', color='green')
ax.plot(temperaturesHigh, valuesHigh, 'o', label='actual off', color='red')

legend = ax.legend(loc='lower right')
for label in legend.get_lines():
    label.set_linewidth(2)
for label in legend.get_texts():
    label.set_fontsize('large')

plt.savefig("plotValue.png")
plt.show()
