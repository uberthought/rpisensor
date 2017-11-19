import RPi.GPIO as GPIO
import time

class Solenoid:

    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(21, GPIO.OUT)
        self.on = False

    def switchOn(self):
        self.on = True
        GPIO.output(21, True)

    def switchOff(self):
        self.on = False
        GPIO.output(21, False)

    def isOn(self):
        return self.on

    def isOff(self):
        return not self.on

