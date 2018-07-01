import pickle
import os.path
import numpy as np
import math
import random
import threading
import csv

class Experiences:
    def __init__(self, filename='experiences'):
        self.pickle_filename = filename + '.p'
        self.csv_filename = filename + '.csv'

    def load(self):
        if os.path.exists(self.pickle_filename):
            saved = pickle.load(open(self.pickle_filename, "rb"))
            self.temperatures = saved.temperatures
            self.humidities = saved.humidities
            self.timestamps = saved.timestamps
        else:
            self.reset()

    def reset(self):
        self.temperatures = np.array([], dtype=np.float)
        self.humidities = np.array([], dtype=np.float)
        self.timestamps = np.array([], dtype=np.str)

    def save(self):
        pickle.dump(self, open(self.pickle_filename, "wb"))

    def append(self, filename='experiences'):
        pickle_filename = filename + '.p'
        if os.path.exists(pickle_filename):
            saved = pickle.load(open(pickle_filename, "rb"))
            self.temperatures = np.append(saved.temperatures, self.temperatures)
            self.humidities = np.append(saved.humidities, self.humidities)
            self.timestamps = np.append(saved.timestamps, self.timestamps)
        pickle.dump(self, open(pickle_filename, "wb"))

    def add(self, temperature, humidity, timestamp):
        self.temperatures = np.concatenate((self.temperatures, [temperature]))
        self.humidities = np.concatenate((self.humidities, [humidity]))
        self.timestamps = np.concatenate((self.timestamps, [timestamp]))

    def saveCSV(self):
        with open(self.csv_filename, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
            spamwriter.writerow(['timestamps', 'temperatures', 'humidities'])
            for x in range(len(self.timestamps)):
                spamwriter.writerow([self.timestamps[x], self.temperatures[x], self.humidities[x]])
