#!/usr/bin/python3

import unittest
import datetime
from Experiences import Experiences

class TestExperiences(unittest.TestCase):
    def test_init(self):
        experiences = Experiences()
        count = len(experiences.get())
        self.assertTrue(count >= 0)

    def test_add(self):
        experiences = Experiences()
        count0 = len(experiences.get())

        temperature = 1.0
        humidity = 1.0
        isOn = True
        timestamp = datetime.datetime.now()

        experiences.add(temperature, humidity, isOn, timestamp)

        count1 = len(experiences.get())
        self.assertEqual(count0 + 1, count1)

if __name__ == '__main__':
    unittest.main()
