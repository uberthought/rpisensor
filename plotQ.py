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

states0, _, _, _ = experiencesFake.get()
temperatures = []
actions = []
triggers = []
for state0 in states0:
    hactions = model.dqn_run([state0])[0]
    temperatures.append(state0[-1])
    actions.append(hactions)
    triggers.append(np.argmax(hactions) / 3)

fig, ax = plt.subplots(figsize=(7, 7))
ax.plot(temperatures, [x[0] for x in actions], label='off', color='blue')
ax.plot(temperatures, [x[1] for x in actions], label='low', color='green')
ax.plot(temperatures, [x[2] for x in actions], label='high', color='red')
ax.plot(temperatures, [x[3] for x in actions], label='ac', color='orange')
ax.plot(temperatures, triggers, label='trigger', color='gray')

# legend = ax.legend(loc='lower right')
# for label in legend.get_lines():
#     label.set_linewidth(0.5)
# for label in legend.get_texts():
#     label.set_fontsize('small')

name = "Q"
if not os.path.exists("plots"):
    os.makedirs("plots")
plt.savefig("plots/"+name+".png")
plt.show()
timestr = time.strftime("%Y%m%d-%H%M%S")
shutil.copyfile("plots/"+name+".png", "plots/"+name+"."+timestr+".png")
