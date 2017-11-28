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
        self.on = False
        self.load()

    def load(self):
        if os.path.exists('solenoid.p'):
            self.on = pickle.load(open("solenoid.p", "rb"))

    def save(self):
        pickle.dump(self.on, open("solenoid.p", "wb"))

    def switchOn(self):
        self.on = True
        GPIO.output(21, True)
        self.save()

    def switchOff(self):
        self.on = False
        GPIO.output(21, False)
        self.save()

    def isOn(self):
        return self.on

    def isOff(self):
        return not self.on

