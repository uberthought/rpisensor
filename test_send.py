#!/usr/bin/python3

from Communication import Communication
from Experiences import Experiences

experiences = Experiences()
communication = Communication()

communication.send('192.168.1.178', experiences)
