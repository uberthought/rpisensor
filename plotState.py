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

target = experiences.experiences[-1].target
temperatures = [x.temperature for x in experiences.experiences]
min = np.min(temperatures)
max = np.max(temperatures)

experiencesFake = Experiences()
experiencesFake.experiences = []
for temperature in np.arange(min, max, .01):
    experiencesFake.add2(temperature, .5, False, 0, target)

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
        temperaturesOff.append(experiences.stateToTemperature(state0))
        state1Off.append(experiences.stateToTemperature(state1))
    else:
        temperaturesOn.append(experiences.stateToTemperature(state0))
        state1On.append(experiences.stateToTemperature(state1))

fooFake = experiencesFake.get()[2:]
predictedOn = []
predictedOff = []
diffOn = []
diffOff = []
temperatures = []
sensor = solenoid = simulation = Simulation.init()

for experience in fooFake:
    state0 = experience.state0

    temperature0 = experiences.stateToTemperature(experience.state0)

    simulation.temperature = temperature0
    simulation.switchOff()
    simulation.step()
    temperature1, _, _ = sensor.gather()
    state10 = experiences.temperatureToState(temperature1, target)

    simulation.temperature = temperature0
    simulation.switchOn()
    simulation.step()
    temperature1, _, _ = sensor.gather()
    state11 = experiences.temperatureToState(temperature1, target)

    states0 = [state0, state0]
    actions = [[0], [1]]
    states1, values = model.model_run(states0, actions)

    temperatures.append(experiences.stateToTemperature(state0))
    predictedOff.append(experiences.stateToTemperature(states1[0]))
    predictedOn.append(experiences.stateToTemperature(states1[1]))
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

plt.savefig("plotState.png")
plt.show()
