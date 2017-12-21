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
min = experiences.experiences[-1].target - experiences.experiences[-1].target_delta
max = experiences.experiences[-1].target + experiences.experiences[-1].target_delta
target = experiences.experiences[-1].target
target_delta = experiences.experiences[-1].target_delta

experiencesFake = Experiences()
experiencesFake.experiences = []
for temperature in np.arange(min, max, .01):
        experiencesFake.add2(temperature, .5, False, 0, target, target_delta)
        experiencesFake.add2(temperature, .5, True, 0, target, target_delta)

fooFake = experiencesFake.get()[2:]
# fooFake = experiences.get()
valuesOn = []
valuesOff = []
temperaturesOn = []
temperaturesOff = []
i = 0
for experience in fooFake:
    _, values = model.model_run([experience.state0], [experience.action])

    if experience.action[0] == 0:
        valuesOff.append(values[0][0])
        # valuesOff.append(experience.value - values[0][0])
        # valuesOff.append(experience.value)
        temperaturesOff.append(experience.state0[2])
    else:
        valuesOn.append(values[0][0])
        # valuesOn.append(experience.value - values[0][0])
        # valuesOn.append(experience.value)
        temperaturesOn.append(experience.state0[2])
    
    if experience.value == -1:
        print(i, experience.state0)
    i += 1

fig, ax = plt.subplots()
ax.plot(temperaturesOn, valuesOn, 'o', label='on')
ax.plot(temperaturesOff, valuesOff, 'o', label='off')

legend = ax.legend(loc='lower right')
for label in legend.get_lines():
    label.set_linewidth(2)
for label in legend.get_texts():
    label.set_fontsize('large')

plt.savefig("plot.png")
plt.show()