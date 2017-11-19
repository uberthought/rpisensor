import RPi.GPIO as GPIO
import time

class Button:
        def __init__(self):
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        def get(self):
                pressed = False
                for i in range(10):
                        input_state = not GPIO.input(11)
                        if input_state:
                                pressed = True
                        time.sleep(0.1)

                if pressed:
                        while input_state:
                                input_state = not GPIO.input(11)
                        time.sleep(0.1)

                return pressed