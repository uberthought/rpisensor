import numpy as np
import os
import time

from network import Model
from Experiences import Experiences
from Settings import Settings

def plotPredictedState(model, experiences, settings):
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

    for i in range(len(values)):
        state0 = states0[i]

        hstates0 = [state0] * Model.action_size
        hactions = np.zeros((Model.action_size, Model.action_size))
        for j in range(Model.action_size):
            hactions[j][j] = 1
        hstates1, hvalues = model.model_run(hstates0, hactions)

        temperature = Experiences.denormalize_temperature(state0[0]) + state0[2]

        off = np.append(off, [[temperature, hstates1[:,-1][0]]], axis=0)
        low = np.append(low, [[temperature, hstates1[:,-1][1]]], axis=0)
        high = np.append(high, [[temperature, hstates1[:,-1][2]]], axis=0)
        ac = np.append(ac, [[temperature, hstates1[:,-1][3]]], axis=0)

    return off, low, high, ac


def plotActualState(model, experiences, settings):
    states0, actions, values, states1 = experiences.get()
    off = np.array([]).reshape(0, 2)
    low = np.array([]).reshape(0, 2)
    high = np.array([]).reshape(0, 2)
    ac = np.array([]).reshape(0, 2)

    for i in range(len(values)):
        state0 = states0[i]
        state1 = states1[i]
        action = actions[i]

        temperature = Experiences.denormalize_temperature(state0[0]) + state0[2]

        if action[0] == 1:
            off = np.append(off, [[temperature, state1[-1]]], axis=0)
        elif action[1] == 1:
            low = np.append(low, [[temperature, state1[-1]]], axis=0)
        elif action[2] == 1:
            high = np.append(high, [[temperature, state1[-1]]], axis=0)
        elif action[3] == 1:
            ac = np.append(ac, [[temperature, state1[-1]]], axis=0)

    return off, low, high, ac