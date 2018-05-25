import pickle
import os.path
import subprocess
import socket
import time
import struct

class Communication:

    PORT = 50008

    def __init__(self):
        self.s = None

    def send(self, host, object):
        if self.s == None:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.connect((host, Communication.PORT))
        data = pickle.dumps(object)
        data = struct.pack('>I', len(data)) + data
        self.s.send(data)
        data = self.s.recv(1024)
        self.s.close()

    def receive(self, host):
        if self.s == None:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.s.bind((host, Communication.PORT))
        self.s.listen(1)
        conn, addr = self.s.accept()
        raw_data = conn.recv(4)
        l = struct.unpack('>I',raw_data)[0]
        data = bytes()
        while len(data) < l:
            raw_data = conn.recv(l - len(data))
            data += raw_data
            if not raw_data: break
        conn.send('ack'.encode())
        conn.close()
        object = pickle.loads(data)
        return object

    def getNetwork(self):

        if not os.path.isdir('train'):
            os.makedirs('train')
        subprocess.call(['scp', '-P 2222', 'root@35.202.235.6:DQN/train/*', 'train/'])