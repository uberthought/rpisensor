#!/usr/bin/python3

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
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

states0, actions, values, states1 = experiences.get()
temperaturesOff = []
state1Off = []
temperaturesLow = []
state1Low = []
temperaturesHigh = []
state1High = []
temperaturesAC = []
state1AC = []

for i in range(len(values)):
    state0 = states0[i]
    state1 = states1[i]
    action = actions[i]

    if action[0] == 1:
        temperaturesOff.append(state0[-1])
        state1Off.append(state1[-1])
    elif action[1] == 1:
        temperaturesLow.append(state0[-1])
        state1Low.append(state1[-1])
    elif action[2] == 1:
        temperaturesHigh.append(state0[-1])
        state1High.append(state1[-1])
    elif action[3] == 1:
        temperaturesAC.append(state0[-1])
        state1AC.append(state1[-1])

states0, actions, values, states1 = experiencesFake.get()
temperatures = []
predicted = []

for i in range(len(values)):
    state0 = states0[i]

    temperature0 = state0[-1]

    hstates0 = [state0] * Model.action_size
    hactions = np.zeros((Model.action_size, Model.action_size))
    for j in range(Model.action_size):
        hactions[j][j] = 1
    hstates1, hvalues = model.model_run(hstates0, hactions)

    temperatures.append(state0[-1])
    predicted.append(hstates1[:,-1])

fig, ax = plt.subplots(figsize=(7, 7))
ax.plot(temperaturesOff, state1Off, '.', label='off', color='blue')
ax.plot(temperaturesLow, state1Low, '.', label='low', color='green')
ax.plot(temperaturesHigh, state1High, '.', label='high', color='red')
ax.plot(temperaturesAC, state1AC, '.', label='ac', color='orange')
ax.plot(temperatures, [x[0] for x in predicted], label='predicted off', color='blue')
ax.plot(temperatures, [x[1] for x in predicted], label='predicted low', color='green')
ax.plot(temperatures, [x[2] for x in predicted], label='predicted high', color='red')
ax.plot(temperatures, [x[3] for x in predicted], label='predicted ac', color='orange')

# legend = ax.legend(loc='lower right')
# for label in legend.get_texts():
#     label.set_fontsize('small')

name = "state"
if not os.path.exists("plots"):
    os.makedirs("plots")
plt.savefig("plots/"+name+".png")
plt.show()
timestr = time.strftime("%Y%m%d-%H%M%S")
shutil.copyfile("plots/"+name+".png", "plots/"+name+"."+timestr+".png")
