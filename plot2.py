#!/usr/bin/python3

# import matplotlib
# matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np

from network import Model
from Experiences import Experience, Experiences

model = Model(2, 2)
experiences = Experiences()

print('experiences ', len(experiences.experiences))

temperatures = [x.temperature for x in experiences.experiences]
min = experiences.experiences[-1].target - experiences.experiences[-1].target_delta
max = experiences.experiences[-1].target + experiences.experiences[-1].target_delta
target = experiences.experiences[-1].target
target_delta = experiences.experiences[-1].target_delta

experiencesFake = Experiences()
experiencesFake.experiences = []
for temperature in np.arange(min, max, .01):
        experiencesFake.add2(temperature, .5, False, 0, target, target_delta)

fooFake = experiencesFake.get()[2:]
# fooFake = experiences.get()
temperatures2 = []
actions2 = []
diff2 = []
for experience in fooFake:

    actions = model.dqn_run([experience.state0])[0]

    temperatures2.append(experience.state1[1])
    actions2.append(actions)
    diff2.append(actions[1] - actions[0])

fig, ax = plt.subplots(figsize=(20, 10))
ax.plot(temperatures2, [x[0] for x in actions2], '.', label='off', color='blue')
ax.plot(temperatures2, [x[1] for x in actions2], '.', label='on', color='red')
ax.plot(temperatures2, diff2, '.', label='diff', color='gray')

legend = ax.legend(loc='lower right')
for label in legend.get_lines():
    label.set_linewidth(2)
for label in legend.get_texts():
    label.set_fontsize('large')

plt.savefig("plot.png")
plt.show()