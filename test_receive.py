#!/usr/bin/python3

from Communication import Communication
from Experiences import Experiences
import time

communication = Communication()

while True:
    experiences = communication.receiveExperiences('')
    print(experiences)
    time.sleep(1)