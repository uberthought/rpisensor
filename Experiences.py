import pickle
import os.path

class Experience:
    def __init__(self, state0, state1, action, value):
        self.state0 = state0
        self.state1 = state1
        self.action = action
        self.value = value

class Experiences:
    def __init__(self):
        self.experiences = []
        if os.path.exists('experiences.p'):
            self.experiences = pickle.load(open("experiences.p", "rb"))

    def add(self, state0, state1, action, value):
        experience = Experience(state0, state1, action, value)
        self.experiences.append(experience)
        pickle.dump(self.experiences, open("experiences.p", "wb"))

    def get(self):
        return self.experiences
