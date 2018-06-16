import RPi.GPIO as GPIO
import time
import pickle
import os.path

class Solenoid:

    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(21, GPIO.OUT)
        GPIO.setup(11, GPIO.OUT)
        GPIO.output(11, True)
        self.power = 0
        self.load()

    def load(self):
        if os.path.exists('solenoid.p'):
            saved = pickle.load(open("solenoid.p", "rb"))
            self.power = saved.power

    def save(self):
        pickle.dump(self, open("solenoid.p", "wb"))

    def switchOn(self):
        GPIO.output(21, True)
        self.save()

    def switchOff(self):
        GPIO.output(21, False)
        self.save()

    def isOn(self):
        return self.power == 2

    def setPower(self, power):
        if power == 2:
            self.switchOn()
        else:
            self.switchOff()
        self.power = power

    def getPower(self):
        return self.power
