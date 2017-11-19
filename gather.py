#!/usr/bin/python3

import os.path
import time
import datetime

from Sensor import Sensor
from Solenoid import Solenoid
from Experiences import Experiences

sensor = Sensor()
solenoid = Solenoid()
experiences = Experiences()

print('experiences ', len(experiences.get()))

for iteration in range(27):

    temperature, humidity, timestamp = sensor.gather()
    isOn = solenoid.isOn()
    experiences.add(temperature, humidity, isOn, timestamp)

    print('temperature', temperature * 9 / 5 + 32, 'humidity', humidity, 'on', isOn, 'time', timestamp)

    time.sleep(5)
