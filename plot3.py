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
        experiencesFake.add2(temperature, .5, True, 0, target, target_delta)


fooFake = experiences.get()
# fooFake = experiencesFake.get()[2:]
valuesOn = []
valuesOff = []
temperaturesOn = []
temperaturesOff = []
diff = []

for experience in fooFake:
    state0 = experience.state0
    action = experience.action
    states1, values = model.model_run([state0], [action])

    if experience.action[0] == 0:
        valuesOff.append(experience.value)
        # valuesOff.append(values[0])
        temperaturesOff.append(experience.state0[1])
    else:
        valuesOn.append(experience.value)
        # valuesOn.append(values[0])
        temperaturesOn.append(experience.state0[1])

fig, ax = plt.subplots(figsize=(20, 10))
ax.plot(temperaturesOff, valuesOff, '.', label='off', color='blue')
ax.plot(temperaturesOn, valuesOn, '.', label='on', color='red')

legend = ax.legend(loc='lower right')
for label in legend.get_texts():
    label.set_fontsize('large')

plt.savefig("plot.png")
plt.show()