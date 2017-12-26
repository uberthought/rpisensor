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
valuesOn = []
valuesOff = []
temperaturesOn = []
temperaturesOff = []
temperatures = []
diff = []
diffOff = []
diffOn = []

for experience in fooFake:
    state0 = experience.state0
    states1, values = model.model_run([state0, state0], [[0], [1]])

    valuesOff.append(values[0][0])
    valuesOn.append(values[1][0])
    temperaturesOff.append(states1[0][1] / 100)
    temperaturesOn.append(states1[1][1] / 100)
    diff.append(values[1][0] - values[0][0])
    diffOff.append(state0[0] - states1[0][1])
    diffOn.append(state0[1] - states1[1][1])
    temperatures.append(experience.state0[1])

fig, ax = plt.subplots(figsize=(20, 10))
ax.plot(temperatures, valuesOff, '.', label='off', color='blue')
ax.plot(temperatures, valuesOn, '.', label='on', color='red')
# ax.plot(temperatures, temperaturesOff, 'o', label='off', color='blue')
# ax.plot(temperatures, temperaturesOn, 'o', label='on', color='red')
# ax.plot(temperatures, diffOff, '.', label='diff off', color='blue')
# ax.plot(temperatures, diffOn, label='diff on', color='red')
ax.plot(temperatures, diff, '.', label='diff', color='gray')

legend = ax.legend(loc='lower right')
for label in legend.get_texts():
    label.set_fontsize('large')

plt.savefig("plot.png")
plt.show()