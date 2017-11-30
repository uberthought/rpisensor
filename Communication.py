import pickle
import os.path
import subprocess

class Communication:
    def sendExperiences():
        if os.path.exists('experiences.p'):
            subprocess.call(['scp', '-P 2222', 'experiences.p', 'root@35.202.235.6:DQN/'])
        # if os.path.exists('settings.p'):
        #     subprocess.call(['scp', '-P 2222', 'settings.p', 'root@35.202.235.6:DQN/'])
    
    def getNetwork():
        if not os.path.isdir('train'):
            os.makedirs('train')
        subprocess.call(['scp', '-P 2222', 'root@35.202.235.6:DQN/train/*', 'train/'])