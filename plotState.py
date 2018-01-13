#!/usr/bin/python3

# import matplotlib
# matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np

from network import Model
from Experiences import Experience, Experiences
from Simulation import Simulation

<<<<<<< HEAD
model = Model()
=======
model = Model(3, 3)
>>>>>>> master
experiences = Experiences()

print('experiences ', len(experiences.experiences))

target = experiences.experiences[-1].target
# temperatures = [x.temperature for x in experiences.experiences]
# min = np.min(temperatures)
# max = np.max(temperatures)
min = target - 1
max = target + 1

experiencesFake = Experiences()
experiencesFake.experiences = []
for temperature in np.arange(min, max, .01):
    experiencesFake.add2(temperature, .5, False, 0, target, Simulation.outside)

fooFake = experiences.get()
temperaturesOff = []
state1Off = []
temperaturesLow = []
state1Low = []
temperaturesHigh = []
state1High = []

for experience in fooFake:
    state0 = experience.state0
    state1 = experience.state1
    action = experience.action

    states0 = [state0]
    actions = [action]
    states1, values = model.model_run(states0, actions)

<<<<<<< HEAD
    if action[0] == 1:
        temperaturesOff.append(state0[-1])
        state1Off.append(state1[-1])
    elif action[1] == 1:
        temperaturesLow.append(state0[-1])
        state1Low.append(state1[-1])
=======
    # print(state0)
    # print(state1)

    if action[0] == 0:
        temperaturesOff.append(experiences.stateToTemperature(state0))
        state1Off.append(experiences.stateToTemperature(state1))
>>>>>>> master
    else:
        temperaturesHigh.append(state0[-1])
        state1High.append(state1[-1])

fooFake = experiencesFake.get()[2:]
temperatures = []
predicted = []

for experience in fooFake:
    state0 = experience.state0

    temperature0 = experience.state0[-1]

<<<<<<< HEAD
    states0 = [state0] * Model.action_size
    actions = np.zeros((Model.action_size, Model.action_size))
    for j in range(Model.action_size):
        actions[j][j] = 1
=======
    states0 = [state0] * 3
    actions = np.arange(3).reshape((3, 1))
>>>>>>> master
    states1, values = model.model_run(states0, actions)

    temperatures.append(state0[-1])
    predicted.append(states1[:,-1])

fig, ax = plt.subplots(figsize=(5, 3.5))
ax.plot(temperaturesOff, state1Off, '.', label='off', color='blue')
ax.plot(temperaturesLow, state1Low, '.', label='low', color='green')
ax.plot(temperaturesHigh, state1High, '.', label='high', color='red')
ax.plot(temperatures, [x[0] for x in predicted], label='predicted off', color='blue')
ax.plot(temperatures, [x[1] for x in predicted], label='predicted low', color='green')
ax.plot(temperatures, [x[2] for x in predicted], label='predicted high', color='red')
ax.plot(temperatures, [x[3] for x in predicted], label='predicted ac', color='orange')

# legend = ax.legend(loc='lower right')
# for label in legend.get_texts():
#     label.set_fontsize('small')

plt.savefig("plotState.png")
plt.show()
