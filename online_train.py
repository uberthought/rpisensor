#!/usr/bin/python3

from Sensor import Sensor
from Solenoid import Solenoid
from network import Model
from Experiences import Experiences, create_state
from Settings import Settings
from Communication import Communication

import time
import numpy as np
import random
import math

class OnlineTrainer:

    def __init__(self):
        self.sensor = Sensor()
        self.solenoid = Solenoid()

        self.experiences = Experiences()
        self.model = Model()
        self.last_state = None

        self.target = 0
        self.temperature = 0
        self.action = 0
        self.reason = ''

        action = 0

    def run_once(self):
        target = Settings.getTargetC()
        exploring = Settings.getExploring()
        temperature, humidity, timestamp, outside = self.sensor.gather()
        self.experiences.add(temperature, humidity, self.solenoid.getPower(), timestamp, target, outside)
        state0 = create_state(target, temperature, outside)

        if exploring and random.random() < 0.2:
            state0 = None

        if (temperature - target) < -1.0:
            self.reason = 'force low'
            action = 2
        elif (temperature - target) > 1.0:
            self.reason = 'force high'
            action = 3
        elif state0 is None:
            self.reason = 'exploring'
            action = np.random.choice(Model.action_size, 1)[0]
        else:
            self.reason = ''
            action = self.model.dqn_run_action([state0])

        self.solenoid.setPower(action)

        self.target = target
        self.temperature = temperature
        self.action = action

        # print(target, temperature, action)
        # print("{0:0.2f}".format(temperature), str(action)+action_type, "{0:0.2f}".format(value), "{0:0.2f}".format(start-last), state0)

    def train_once(self):
        model_loss = self.model.model_train(self.experiences, True)
        dqn_loss = self.model.dqn_train(self.experiences, True)
        self.model.save()

        print(model_loss, dqn_loss)

        return model_loss, dqn_loss

    def send_experiences(self):
        if len(self.experiences.states0) > 1:
            try:
                communication = Communication()
                communication.send('35.232.250.6', self.experiences)
                self.experiences.reset()
            except (ConnectionRefusedError, ConnectionResetError):
                pass

    def pending_experience_count(self):
        return len(self.experiences.timestamps)


# trainer = OnlineTrainer()
# trainer.run_once()
# trainer.train_once()
