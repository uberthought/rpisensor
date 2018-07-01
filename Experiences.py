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
            self.timestamps = saved.timestamps
            self.temperatures = saved.temperatures
            self.humidities = saved.humidities
            self.pm25s = saved.pm25s
            self.pm10s = saved.pm10s
        else:
            self.reset()

    def reset(self):
        self.timestamps = np.array([], dtype=np.str)
        self.temperatures = np.array([], dtype=np.float)
        self.humidities = np.array([], dtype=np.float)
        self.pm25s = np.array([], dtype=np.float)
        self.pm10s = np.array([], dtype=np.float)

    def save(self):
        pickle.dump(self, open(self.pickle_filename, "wb"))

    def append(self, filename='experiences'):
        pickle_filename = filename + '.p'
        if os.path.exists(pickle_filename):
            saved = pickle.load(open(pickle_filename, "rb"))
            self.timestamps = np.append(saved.timestamps, self.timestamps)
            self.temperatures = np.append(saved.temperatures, self.temperatures)
            self.humidities = np.append(saved.humidities, self.humidities)
            self.pm25s = np.append(saved.pm25s, self.pm25s)
            self.pm10s = np.append(saved.pm10s, self.pm10s)
        pickle.dump(self, open(pickle_filename, "wb"))

    def add(self, timestamp, temperature, humidity, pm25, pm10):
        self.timestamps = np.concatenate((self.timestamps, [timestamp]))
        self.temperatures = np.concatenate((self.temperatures, [temperature]))
        self.humidities = np.concatenate((self.humidities, [humidity]))
        self.pm25s = np.concatenate((self.pm25s, [pm25]))
        self.pm10s = np.concatenate((self.pm10s, [pm10]))

    def saveCSV(self):
        with open(self.csv_filename, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
            spamwriter.writerow(['timestamps', 'temperatures', 'humidities', 'pm25', 'pm10'])
            for x in range(len(self.timestamps)):
                spamwriter.writerow([self.timestamps[x], self.temperatures[x], self.humidities[x], self.pm25s[x], self.pm10s[x]])
