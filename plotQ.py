#!/usr/bin/python3

# import matplotlib
# matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np

from network import Model
from Experiences import Experience, Experiences

model = Model()
experiences = Experiences()

print('experiences ', len(experiences.experiences))

target = experiences.experiences[-1].target
# temperatures = [x.temperature for x in experiences.experiences]
# min = np.min(temperatures)
# max = np.max(temperatures)
min = target - 0.5
max = target + 0.5


experiencesFake = Experiences()
experiencesFake.experiences = []
for temperature in np.arange(min, max, .01):
        experiencesFake.add2(temperature, .5, False, 0, target)

fooFake = experiencesFake.get()[2:]
temperatures = []
actions2 = []
triggers = []
for experience in fooFake:
    actions = model.dqn_run([experience.state0])[0]
    temperatures.append(experience.state1[-1])
    actions2.append(actions)
    triggers.append(np.argmax(actions) / 3)

fig, ax = plt.subplots(figsize=(20, 10))
ax.plot(temperatures, [x[0] for x in actions2], label='off', color='blue')
ax.plot(temperatures, [x[1] for x in actions2], label='low', color='green')
ax.plot(temperatures, [x[2] for x in actions2], label='high', color='red')
ax.plot(temperatures, [x[3] for x in actions2], label='ac', color='orange')
ax.plot(temperatures, triggers, label='trigger', color='gray')

legend = ax.legend(loc='lower right')
for label in legend.get_lines():
    label.set_linewidth(2)
for label in legend.get_texts():
    label.set_fontsize('large')

plt.savefig("plotQ.png")
plt.show()
