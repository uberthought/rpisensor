#!/usr/bin/python3

import unittest
import time
from Solenoid import Solenoid

class TestSolenoid(unittest.TestCase):
    def test_isOn(self):
        solenoid = Solenoid()
        isOn = solenoid.isOn()
        self.assertFalse(isOn)

        time.sleep(1)

        solenoid.switchOn()
        isOn = solenoid.isOn()
        self.assertTrue(isOn)

        time.sleep(1)

        solenoid.switchOff()
        isOn = solenoid.isOn()
        self.assertFalse(isOn)

    def test_isOff(self):
        solenoid = Solenoid()
        isOff = solenoid.isOff()
        self.assertTrue(isOff)

        time.sleep(1)

        solenoid.switchOn()
        isOff = solenoid.isOff()
        self.assertFalse(isOff)

        time.sleep(1)

        solenoid.switchOff()
        isOff = solenoid.isOff()
        self.assertTrue(isOff)

if __name__ == '__main__':
    unittest.main()
