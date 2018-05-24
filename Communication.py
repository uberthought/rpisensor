import pickle
import os.path
import subprocess
import socket

HOST = ''                 # Symbolic name meaning the local host
PORT = 50007              # Arbitrary non-privileged port

class Communication:
    def sendExperiences(self, experiences):
        print('sendExperiences')
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        data = pickle.dumps(experiences)
        s.send(data)
        data = s.recv(1024)
        s.close()
        # print('Reply', repr(data))

    def receiveExperiences(self):
        print('receiveExperiences')
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        s.listen(1)
        conn, addr = s.accept()
        print ('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data: break
            conn.send('ack'.encode())
            # print('Received', repr(data))
            experiences = pickle.loads(data)
            # print(experiences)
        conn.close()
        return experiences

    def getNetwork(self):
        if not os.path.isdir('train'):
            os.makedirs('train')
        subprocess.call(['scp', '-P 2222', 'root@35.202.235.6:DQN/train/*', 'train/'])