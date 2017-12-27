#!/usr/bin/python3

# import matplotlib
# matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np

from network import Model
from Experiences import Experience, Experiences
from Simulation import Simulation

model = Model(3, 2)
experiences = Experiences()

print('experiences ', len(experiences.experiences))

# temperatures = [x.temperature for x in experiences.experiences]
# min = np.min(temperatures)
# max = np.max(temperatures)
min = experiences.experiences[-1].target - experiences.experiences[-1].target_delta
max = experiences.experiences[-1].target + experiences.experiences[-1].target_delta
target = experiences.experiences[-1].target
target_delta = experiences.experiences[-1].target_delta


experiencesFake = Experiences()
experiencesFake.experiences = []
for temperature in np.arange(min, max, .01):
    experiencesFake.add2(temperature, .5, False, 0, target, target_delta)

fooFake = experiences.get()
state1On = []
state1Off = []
temperaturesOn = []
temperaturesOff = []

for experience in fooFake:
    state0 = experience.state0
    state1 = experience.state1
    action = experience.action

    states0 = [state0]
    actions = [action]
    states1, values = model.model_run(states0, actions)

    if action[0] == 0:
        temperaturesOff.append(state0[2])
        state1Off.append(state1[2])
    else:
        temperaturesOn.append(state0[2])
        state1On.append(state1[2])

fooFake = experiencesFake.get()[2:]
predictedOn = []
predictedOff = []
diffOn = []
diffOff = []
temperatures = []
sensor = solenoid = simulation = Simulation.init()

for experience in fooFake:
    state0 = experience.state0

    temperature0 = experience.state0[2] * (Experience.maxTemperature - Experience.minTemperature) + target

    simulation.temperature = temperature0
    simulation.switchOff()
    simulation.step()
    temperature1, _, _ = sensor.gather()
    state10 = (temperature1 - target) / (Experience.maxTemperature - Experience.minTemperature)

    simulation.temperature = temperature0
    simulation.switchOn()
    simulation.step()
    temperature1, _, _ = sensor.gather()
    state11 = (temperature1 - target) / (Experience.maxTemperature - Experience.minTemperature)

    states0 = [state0, state0]
    actions = [[0], [1]]
    states1, values = model.model_run(states0, actions)

    temperatures.append(state0[2])
    predictedOff.append(states1[0][2])
    predictedOn.append(states1[1][2])
    diffOff.append(states1[0][2] - state10)
    diffOn.append(states1[1][2] - state11)

fig, ax = plt.subplots(figsize=(20, 10))
ax.plot(temperaturesOn, state1On, 'o', label='on', color='red')
ax.plot(temperaturesOff, state1Off, 'o', label='off', color='blue')
ax.plot(temperatures, predictedOn, label='predicted on', color='red')
ax.plot(temperatures, predictedOff, label='predicted off', color='blue')
# ax.plot(temperatures, diffOn, label='diff on', color='red')
# ax.plot(temperatures, diffOff, label='diff off', color='blue')

legend = ax.legend(loc='lower right')
for label in legend.get_texts():
    label.set_fontsize('large')

plt.savefig("plot.png")
plt.show()