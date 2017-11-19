import pickle
import os.path

class Experiences:
    def __init__(self):
        self.experiences = []
        if os.path.exists('experiences.p'):
            self.experiences = pickle.load(open("experiences.p", "rb"))

    def add(self, temperature, humidity, isOn, timestamp):
        experience = {'temperature': temperature, 'humidity': humidity, 'isOn': isOn, 'timestamp': timestamp}
        self.experiences.append(experience)
        pickle.dump(self.experiences, open("experiences.p", "wb"))

    def get(self):
        return self.experiences
