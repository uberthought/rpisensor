#!/usr/bin/python3

# import os.path
import time
# import datetime

# from Sensor import Sensor
# from Solenoid import Solenoid

from Simulation import Simulation
from Experiences import Experiences

# sensor = Sensor()
# solenoid = Solenoid()
experiences = Experiences()
simulation = Simulation()

print('experiences ', len(experiences.get()))

temperature, humidity, timestamp = simulation.step()
state_list = [temperature] * 4

for iteration in range(27):

    # temperature, humidity, timestamp = sensor.gather()
    # isOn = solenoid.isOn()

    temperature, humidity, timestamp = simulation.step()
    isOn = simulation.isOn()

    del state_list[0]
    state_list.append(temperature)

    experiences.add(temperature, humidity, isOn, timestamp)

    print('states', state_list, 'humidity', humidity, 'on', isOn, 'time', timestamp)

    # time.sleep(5)
