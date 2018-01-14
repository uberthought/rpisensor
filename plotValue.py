#!/usr/bin/python3

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
import math
import os
import time
import shutil

from network import Model
from Experiences import Experiences
from Simulation import Simulation
from Settings import Settings

model = Model()
experiences = Experiences()
settings = Settings()

target = settings.target
min = target - 1
max = target + 1

experiencesFake = Experiences()
experiencesFake.reset()
for temperature in np.arange(min, max, .01):
    experiencesFake.add2(temperature, .5, False, 0, target, Simulation.outside)

states0, actions, values, states1 = experiencesFake.get()
temperatures = []
predicted = []

for state0 in states0:
    states0 = [state0] * Model.action_size
    actions = np.zeros((Model.action_size, Model.action_size))
    for j in range(Model.action_size):
        actions[j][j] = 1
    states1, values = model.model_run(states0, actions)

    temperatures.append(state0[-1])
    predicted.append(values[:,0])

states0, actions, values, states1 = experiences.get()
temperaturesOff = []
valuesOff = []
temperaturesLow = []
valuesLow = []
temperaturesHigh = []
valuesHigh = []
temperaturesAC = []
valuesAC = []

for i in range(len(values)):
    state0 = states0[i]
    value = values[i]
    action = actions[i]

    # if math.fabs(state0[-1]) > 1 or state0[1] != Simulation.outside:
    #     continue

    if action[0] == 1:
        temperaturesOff.append(state0[-1])
        valuesOff.append(value)
    elif action[1] == 1:
        temperaturesLow.append(state0[-1])
        valuesLow.append(value)
    elif action[2] == 1:
        temperaturesHigh.append(state0[-1])
        valuesHigh.append(value)
    elif action[3] == 1:
        temperaturesAC.append(state0[-1])
        valuesAC.append(value)


fig, ax = plt.subplots(figsize=(7, 7))
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

name = "value"
if not os.path.exists("plots"):
    os.makedirs("plots")
plt.savefig("plots/"+name+".png")
plt.show()
timestr = time.strftime("%Y%m%d-%H%M%S")
shutil.copyfile("plots/"+name+".png", "plots/"+name+"."+timestr+".png")
