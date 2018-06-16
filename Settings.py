import pickle
import os.path
import random

def toF(c):
    return float(c) * 9 / 5 + 32

def toC(f):
    return (float(f) - 32) * 5 / 9

class Settings:
    def __init__(self):
        self.target = 24
        self.on = True
        self.gathering = True
        self.training = False
        self.exploring = False
        self.exploration_rate = 0.2
        self.load()
    
    def load(self):
        if os.path.exists('settings.p'):
            settings = pickle.load(open("settings.p", "rb"))
            self.target = settings.target
            self.on = settings.on
            self.gathering = settings.gathering
            self.training = settings.training
            self.exploring = settings.exploring
            self.exploration_rate = settings.exploration_rate

    def save(self):
        pickle.dump(self, open("settings.p", "wb"))

    def setOn(on):
        settings.load()
        settings.on = on
        settings.save()

    def getOn():
        settings.load()
        return settings.on

    def setGathering(gathering):
        settings.load()
        settings.gathering = gathering
        settings.save()

    def getGathering():
        settings.load()
        return settings.gathering

    def setTraining(training):
        settings.load()
        settings.training = training
        settings.save()

    def getTraining():
        settings.load()
        return settings.training

    def setExploring(exploring):
        settings.load()
        settings.exploring = exploring
        settings.save()

    def getExploring():
        settings.load()
        return settings.exploring

    def setExplorationRate(exploration_rate):
        settings.load()
        settings.exploration_rate = exploration_rate
        settings.save()

    def getExplorationRate():
        settings.load()
        return settings.exploration_rate

    def setTargetF(target): 
        settings.load()
        settings.target = toC(target)
        settings.save()

    def getTargetF():
        settings.load()
        return toF(settings.target)

    def getTargetC():
        settings.load()
        return settings.target

settings = Settings()

