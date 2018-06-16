import pickle
import os.path
import random

class Settings:
    def __init__(self):
        self.on = True
        self.collection_rate = 5.0
        self.load()
    
    def load(self):
        if os.path.exists('settings.p'):
            settings = pickle.load(open("settings.p", "rb"))
            self.on = settings.on
            self.collection_rate = settings.collection_rate

    def save(self):
        pickle.dump(self, open("settings.p", "wb"))