#!/usr/bin/python3

from Experiences import Experiences
import numpy as np

experiences = Experiences()

print('experiences ', len(experiences.timestamps))

experiences.saveCSV()