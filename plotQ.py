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

# min = experiences.experiences[-1].target - experiences.experiences[-1].target_delta
# max = experiences.experiences[-1].target + experiences.experiences[-1].target_delta
temperatures = [x.temperature for x in experiences.experiences]
min = np.min(temperatures)
max = np.max(temperatures)
target = experiences.experiences[-1].target
target_delta = experiences.experiences[-1].target_delta

experiencesFake = Experiences()
experiencesFake.experiences = []
for temperature in np.arange(min, max, .01):
        experiencesFake.add2(temperature, .5, False, 0, target, target_delta)

fooFake = experiencesFake.get()[2:]
temperatures = []
actions2 = []
triggers = []
diff = []
for experience in fooFake:
    actions = model.dqn_run([experience.state0])[0]
    temperatures.append(experience.state1[2])
    actions2.append(actions)
    triggers.append(np.sign(actions[1] - actions[0]))
    diff.append(actions[1] - actions[0])

fig, ax = plt.subplots(figsize=(20, 10))
ax.plot(temperatures, [x[0] for x in actions2], label='off', color='blue')
ax.plot(temperatures, [x[1] for x in actions2], label='on', color='red')
# ax.plot(temperatures, triggers, label='trigger', color='gray')
# ax.plot(temperatures, diff, label='on vs. off', color='gray')

legend = ax.legend(loc='lower right')
for label in legend.get_lines():
    label.set_linewidth(2)
for label in legend.get_texts():
    label.set_fontsize('large')

plt.savefig("plotQ.png")
plt.show()
