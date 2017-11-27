import pickle
import os.path

def toF(c):
    return float(c) * 9 / 5 + 32

def toC(f):
    return (float(f) - 32) * 5 / 9

class Settings:
    def __init__(self):
        self.target = 24.0
        self.target_delta = 0.5
        self.on = False
        self.load()
    
    def load(self):
        if os.path.exists('settings.p'):
            settings = pickle.load(open("settings.p", "rb"))
            self.target = settings.target
            self.target_delta = settings.target_delta
            self.on = settings.on

    def save(self):
        pickle.dump(self, open("settings.p", "wb"))

    def setOn(self, on): 
        self.on = on
        self.save()

    def getOn(self):
        self.load()
        return self.on

    def setTargetF(self, target): 
        self.target = toC(target)
        self.save()

    def getTargetF(self):
        self.load()
        return toF(self.target)

    def getTargetC(self):
        self.load()
        return self.target

    def getTargetDelta(self):
        self.load()
        return self.target_delta

