#!/usr/bin/python3

import numpy as np
import os
import time

from network import Model
from Experiences import Experiences
from Settings import Settings

def plotQ(model, experiences, settings):
    target = settings.target
    min = target - 1
    max = target + 1

    experiencesFake = Experiences()
    experiencesFake.reset()
    for temperature in np.arange(min, max, .01):
        experiencesFake.add2(temperature, .5, False, 0, target, 0)

    states0, _, _, _ = experiencesFake.get()
    temperatures = []
    off = []
    low = []
    high = []
    ac = []

    for state0 in states0:

        hactions = model.dqn_run([state0])[0]

        temperatures.append(state0[-1])
        off.append(hactions[0])
        low.append(hactions[1])
        high.append(hactions[2])
        ac.append(hactions[3])

    return temperatures, off, low, high, ac
