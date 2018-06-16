#!/usr/bin/python3

import numpy as np
import math
import os
import time

from network import Model
from Experiences import Experiences, normalize_temperature
from Settings import Settings

def plotPredictedValue(model, experiences, settings):
    target = 28.8889
    min = target - 1
    max = target + 1

    experiencesFake = Experiences()
    experiencesFake.reset()
    for temperature in np.arange(min, max, .01):
        experiencesFake.add2(temperature, .5, False, 0, target, 0)

    states0, actions, values, states1 = experiencesFake.get()

    off = np.array([]).reshape(0, 2)
    low = np.array([]).reshape(0, 2)
    high = np.array([]).reshape(0, 2)
    ac = np.array([]).reshape(0, 2)

    for state0 in states0:
        states0 = [state0] * Model.action_size
        actions = np.zeros((Model.action_size, Model.action_size))
        for j in range(Model.action_size):
            actions[j][j] = 1
        states1, values = model.model_run(states0, actions)

        temperature = Experiences.denormalize_temperature(state0[0]) + state0[2]

        off = np.append(off, [[temperature, values[:,0][0]]], axis=0)
        low = np.append(low, [[temperature, values[:,0][1]]], axis=0)
        high = np.append(high, [[temperature, values[:,0][2]]], axis=0)
        ac = np.append(ac, [[temperature, values[:,0][3]]], axis=0)

    return off, low, high, ac

def plotActualValue(model, experiences, settings):
    states0, actions, values, states1 = experiences.get()

    off = np.array([]).reshape(0, 2)
    low = np.array([]).reshape(0, 2)
    high = np.array([]).reshape(0, 2)
    ac = np.array([]).reshape(0, 2)

    for i in range(len(values)):
        state0 = states0[i]
        value = values[i]
        action = actions[i]

        temperature = Experiences.denormalize_temperature(state0[0]) + state0[2]

        if action[0] == 1:
            off = np.append(off, [[temperature, value]], axis=0)
        elif action[1] == 1:
            low = np.append(low, [[temperature, value]], axis=0)
        elif action[2] == 1:
            high = np.append(high, [[temperature, value]], axis=0)
        elif action[3] == 1:
            ac = np.append(ac, [[temperature, value]], axis=0)

    return off, low, high, ac