#!/usr/bin/python3

# import matplotlib
# matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
import math

from network import Model
from Experiences import Experience, Experiences
from Simulation import Simulation

<<<<<<< HEAD
model = Model()
=======
model = Model(3, 3)
>>>>>>> master
experiences = Experiences()

print('experiences ', len(experiences.experiences))

target = experiences.experiences[-1].target
# temperatures = [x.temperature for x in experiences.experiences]
# min = np.min(temperatures)
# max = np.max(temperatures)
min = target - 1
max = target + 1

experiencesFake = Experiences()
experiencesFake.experiences = []
for temperature in np.arange(min, max, .01):
    experiencesFake.add2(temperature, .5, False, 0, target, Simulation.outside)

fooFake = experiencesFake.get()[2:]
temperatures = []
predicted = []

for experience in fooFake:
    state0 = experience.state0

    states0 = [state0] * Model.action_size
    actions = np.zeros((Model.action_size, Model.action_size))
    for j in range(Model.action_size):
        actions[j][j] = 1
    states1, values = model.model_run(states0, actions)

    temperatures.append(experience.state0[-1])
    predicted.append(values[:,0])

fooFake = experiences.get()
temperaturesOff = []
valuesOff = []
temperaturesLow = []
valuesLow = []
temperaturesHigh = []
valuesHigh = []
temperaturesAC = []
valuesAC = []

for experience in fooFake:
    state0 = experience.state0
    value = experience.value

    if math.fabs(state0[-1]) > 1 or state0[1] != Simulation.outside:
        continue

    if experience.action[0] == 1:
        temperaturesOff.append(state0[-1])
        valuesOff.append(value)
    elif experience.action[1] == 1:
        temperaturesLow.append(state0[-1])
        valuesLow.append(value)
    elif experience.action[2] == 1:
        temperaturesHigh.append(state0[-1])
        valuesHigh.append(value)
    elif experience.action[3] == 1:
        temperaturesAC.append(state0[-1])
        valuesAC.append(value)


fig, ax = plt.subplots(figsize=(5, 3.5))
ax.plot(temperatures, [x[0] for x in predicted], label='predicted off', color='blue')
ax.plot(temperatures, [x[1] for x in predicted], label='predicted low', color='green')
ax.plot(temperatures, [x[2] for x in predicted], label='predicted high', color='red')
ax.plot(temperatures, [x[3] for x in predicted], label='predicted ac', color='orange')
ax.plot(temperaturesOff, valuesOff, '.', label='actual off', color='blue')
ax.plot(temperaturesLow, valuesLow, '.', label='actual low', color='green')
ax.plot(temperaturesHigh, valuesHigh, '.', label='actual high', color='red')
ax.plot(temperaturesAC, valuesAC, '.', label='actual ac', color='orange')

# legend = ax.legend(loc='lower right')
# for label in legend.get_lines():
#     label.set_linewidth(0.5)
# for label in legend.get_texts():
#     label.set_fontsize('xx-small')

plt.savefig("plotValue.png")
plt.show()
