#!/usr/bin/python3

import datetime
import unittest

from Sensor import Sensor

class TestSensor(unittest.TestCase):
    def test_gather(self):
        sensor = Sensor()
        temperature, humidity, timestamp = sensor.gather()
        delta = datetime.datetime.now() - timestamp
        self.assertTrue(temperature > 0)
        self.assertTrue(temperature < 100)
        self.assertTrue(humidity > 0)
        self.assertTrue(humidity < 100)
        self.assertEqual(delta.days, 0)
        self.assertEqual(delta.seconds, 0)
        self.assertTrue(delta.microseconds > 0)
        self.assertTrue(delta.microseconds < 1000)
        
    
if __name__ == '__main__':
    unittest.main()
