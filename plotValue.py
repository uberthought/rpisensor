#!/usr/bin/python3

import numpy as np
import math
import os
import time

from network import Model
from Experiences import Experiences, normalize_temperature
from Settings import Settings

model = Model()
experiences = Experiences()
settings = Settings()

def plotValue(model, experiences, settings):

    target = settings.target
    min = target - 1
    max = target + 1

    experiencesFake = Experiences()
    experiencesFake.reset()
    for temperature in np.arange(min, max, .01):
        experiencesFake.add2(temperature, .5, False, 0, target, 0)

    states0, actions, values, states1 = experiencesFake.get()
    temperatures = []
    predicted_off = []
    predicted_low = []
    predicted_high = []
    predicted_ac = []

    for state0 in states0:
        states0 = [state0] * Model.action_size
        actions = np.zeros((Model.action_size, Model.action_size))
        for j in range(Model.action_size):
            actions[j][j] = 1
        states1, values = model.model_run(states0, actions)

        temperatures.append(state0[-1])
        predicted_off.append(values[:,0][0])
        predicted_low.append(values[:,0][1])
        predicted_high.append(values[:,0][2])
        predicted_ac.append(values[:,0][3])

    states0, actions, values, states1 = experiences.get()
    temperaturesOff = []
    valuesOff = []
    temperaturesLow = []
    valuesLow = []
    temperaturesHigh = []
    valuesHigh = []
    temperaturesAC = []
    valuesAC = []

    for i in range(len(values)):
        state0 = states0[i]
        value = values[i]
        action = actions[i]

        if state0[0] != normalize_temperature(target):
            continue

        if state0[1] != normalize_temperature(0):
            continue

        if state0[3] - normalize_temperature(target) > 1:
            continue
        if state0[3] - normalize_temperature(target) < -1:
            continue

        if action[0] == 1:
            temperaturesOff.append(state0[-1])
            valuesOff.append(value)
        elif action[1] == 1:
            temperaturesLow.append(state0[-1])
            valuesLow.append(value)
        elif action[2] == 1:
            temperaturesHigh.append(state0[-1])
            valuesHigh.append(value)
        elif action[3] == 1:
            temperaturesAC.append(state0[-1])
            valuesAC.append(value)

    return temperatures, predicted_off, predicted_low, predicted_high, predicted_ac


# ax.plot(temperatures, [x[0] for x in predicted], label='predicted off', color='blue')
# ax.plot(temperatures, [x[1] for x in predicted], label='predicted low', color='green')
# ax.plot(temperatures, [x[2] for x in predicted], label='predicted high', color='red')
# ax.plot(temperatures, [x[3] for x in predicted], label='predicted ac', color='orange')
# ax.plot(temperaturesOff, valuesOff, '.', label='actual off', color='blue')
# ax.plot(temperaturesLow, valuesLow, '.', label='actual low', color='green')
# ax.plot(temperaturesHigh, valuesHigh, '.', label='actual high', color='red')
# ax.plot(temperaturesAC, valuesAC, '.', label='actual ac', color='orange')
