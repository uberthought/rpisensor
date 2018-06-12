#!/usr/bin/python3

import numpy as np
import os
import time

from network import Model
from Experiences import Experiences
from Settings import Settings

def plotQ(model, experiences, settings):
    target = 28.8889
    min = target - 0.5
    max = target + 0.5

    experiencesFake = Experiences()
    experiencesFake.reset()
    for temperature in np.arange(min, max, .01):
        experiencesFake.add2(temperature, .5, False, 0, target, 0)

    states0, _, _, _ = experiencesFake.get()
    off = np.array([]).reshape(0, 2)
    low = np.array([]).reshape(0, 2)
    high = np.array([]).reshape(0, 2)
    ac = np.array([]).reshape(0, 2)


    for state0 in states0:

        hactions = model.dqn_run([state0])[0]
        temperature = Experiences.denormalize_temperature(state0[0]) + state0[2]

        off = np.append(off, [[temperature, hactions[0]]], axis=0)
        low = np.append(low, [[temperature, hactions[1]]], axis=0)
        high = np.append(high, [[temperature, hactions[2]]], axis=0)
        ac = np.append(ac, [[temperature, hactions[3]]], axis=0)

    return off, low, high, ac
