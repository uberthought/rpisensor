#!/usr/bin/python3

from Experiences import Experiences
import numpy as np

experiences = Experiences()

training_data = experiences.get()

print(training_data)
print('experiences ', len(training_data[0]))