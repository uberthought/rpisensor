import pickle
import os.path
import numpy as np
import math
import random
import threading
import csv

class Experiences:
    def __init__(self):
        if os.path.exists('experiences.p'):
            saved = pickle.load(open("experiences.p", "rb"))
            self.temperatures = saved.temperatures
            self.humidities = saved.humidities
            self.timestamps = saved.timestamps
        else:
            self.reset()
            self.save()

    def reset(self):
        self.temperatures = np.array([], dtype=np.float)
        self.humidities = np.array([], dtype=np.float)
        self.timestamps = np.array([], dtype=np.str)

    def save(self):
        pickle.dump(self, open("experiences.p", "wb"))

    def append(self):
        if os.path.exists('experiences.p'):
            saved = pickle.load(open("experiences.p", "rb"))
            self.temperatures = np.append(saved.temperatures, self.temperatures)
            self.humidities = np.append(saved.humidities, self.humidities)
            self.timestamps = np.append(saved.timestamps, self.timestamps)
        pickle.dump(self, open("experiences.p", "wb"))

    def add(self, temperature, humidity, timestamp):
        self.temperatures = np.concatenate((self.temperatures, [temperature]))
        self.humidities = np.concatenate((self.humidities, [humidity]))
        self.timestamps = np.concatenate((self.timestamps, [timestamp]))

    def saveCSV(self):
        with open('experiences.csv', 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
            spamwriter.writerow(['timestamps', 'temperatures', 'humidities'])
            for x in range(len(self.timestamps)):
                spamwriter.writerow([self.timestamps[x], self.temperatures[x], self.humidities[x]])
