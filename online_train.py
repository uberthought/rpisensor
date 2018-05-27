#!/usr/bin/python3

from Sensor import Sensor
from Solenoid import Solenoid
from network import Model
from Experiences import Experiences
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

        action = 0

    def run_once(self):
        target = Settings.getTargetC()
        exploring = Settings.getExploring()
        temperature, humidity, timestamp, outside = self.sensor.gather()
        self.experiences.add(temperature, humidity, self.solenoid.getPower(), timestamp, target, outside)
        state0, _, _, _ = self.experiences.last()

        if exploring and random.random() < 0.2:
            state0 = None

        if (temperature - target) < -1.0:
            action = 2
        elif (temperature - target) > 1.0:
            action = 3
        elif state0 is None:
            action = np.random.choice(Model.action_size, 1)[0]
        else:
            action = self.model.dqn_run_action([state0])

        self.solenoid.setPower(action)

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
                communication.send('192.168.1.178', self.experiences)
                self.experiences.reset()
            except (ConnectionRefusedError, ConnectionResetError):
                pass


# trainer = OnlineTrainer()
# trainer.run_once()
# trainer.train_once()