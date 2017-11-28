import pickle
import os.path

def toF(c):
    return float(c) * 9 / 5 + 32

def toC(f):
    return (float(f) - 32) * 5 / 9

class Settings:
    def __init__(self):
        self.target = toC(75)
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

    def setOn(on):
        settings.load()
        settings.on = on
        settings.save()

    def getOn():
        settings.load()
        return settings.on

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

    def getTargetDelta():
        settings.load()
        return settings.target_delta

settings = Settings()

