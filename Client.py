#!/usr/bin/python3

from threading import Thread
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import cgi
import math

from Settings import Settings
from Sensor import Sensor
from Solenoid import Solenoid

from online_train import OnlineTrainer

trainer = OnlineTrainer()

class WebServer(BaseHTTPRequestHandler):

    def do_GET(self):

        self.showRoot(self.getState())

    def do_POST(self):

        ctype, pdict = cgi.parse_header(self.headers['content-type'])

        if ctype == 'multipart/form-data':
            postvars = cgi.parse_multipart(self.rfile, pdict)
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers['content-length'])
            postvars = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
        else:
            postvars = {}

        print(postvars)

        if b'gathering' in postvars.keys():
            self.gatheringButton()
        if b'training' in postvars.keys():
            self.trainingButton()
        if b'warmer' in postvars.keys():
            self.warmerButton()
        if b'cooler' in postvars.keys():
            self.coolerButton()
        if b'power' in postvars.keys():
            self.powerButton()
        if b'exploring' in postvars.keys():
            self.exploringButton()


    def showRoot(self, message):

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        with open('Client.html', 'r') as indexfile:
            self.wfile.write(bytes(indexfile.read(), 'utf-8'))

        self.wfile.write(bytes('<script>', 'utf-8'))
    
        self.wfile.write(bytes('document.getElementById("message").innerHTML = "' + message + '";', 'utf-8'))
    
        self.wfile.write(bytes('document.getElementById("target").innerHTML = "' + str(Settings.getTargetF()) + '";', 'utf-8'))
    
        if Settings.getGathering():
            self.wfile.write(bytes('document.getElementById("gathering").value = "Stop Gathering";', 'utf-8'))
        else:
            self.wfile.write(bytes('document.getElementById("gathering").value = "Start Gathering";', 'utf-8'))
    
        if Settings.getExploring():
            self.wfile.write(bytes('document.getElementById("exploring").value = "Stop Exploring";', 'utf-8'))
        else:
            self.wfile.write(bytes('document.getElementById("exploring").value = "Start Exploring";', 'utf-8'))
    
        if Settings.getTraining():
            self.wfile.write(bytes('document.getElementById("training").value = "Stop Training";', 'utf-8'))
        else:
            self.wfile.write(bytes('document.getElementById("training").value = "Start Training";', 'utf-8'))
    
        if Settings.getOn():
            self.wfile.write(bytes('document.getElementById("power").value = "Turn Off";', 'utf-8'))
            self.wfile.write(bytes('document.getElementById("gathering").disabled = false;', 'utf-8'))
            self.wfile.write(bytes('document.getElementById("training").disabled = false;', 'utf-8'))
            self.wfile.write(bytes('document.getElementById("exploring").disabled = false;', 'utf-8'))
        else:
            self.wfile.write(bytes('document.getElementById("power").value = "Turn On";', 'utf-8'))
            self.wfile.write(bytes('document.getElementById("gathering").disabled = true;', 'utf-8'))
            self.wfile.write(bytes('document.getElementById("training").disabled = true;', 'utf-8'))
            self.wfile.write(bytes('document.getElementById("exploring").disabled = true;', 'utf-8'))
    
        self.wfile.write(bytes('</script>', 'utf-8'))

    def warmerButton(self):
        Settings.setTargetF(Settings.getTargetF() + 1)
        self.showRoot(self.getState())

    def coolerButton(self):
        Settings.setTargetF(Settings.getTargetF() - 1)
        self.showRoot(self.getState())

    def powerButton(self):
        Settings.setOn(not Settings.getOn())
        solenoid = Solenoid()
        solenoid.switchOff()
        self.showRoot(self.getState())

    def gatheringButton(self):
        Settings.setGathering(not Settings.getGathering())
        self.showRoot(self.getState())

    def trainingButton(self):
        Settings.setTraining(not Settings.getTraining())
        self.showRoot(self.getState())

    def exploringButton(self):
        Settings.setExploring(not Settings.getExploring())
        self.showRoot(self.getState())

    def getState(self):
        message = ''

        try:
            sensor = Sensor()
            solenoid = Solenoid()
            temperature, _, _, _ = sensor.gather()
            f = temperature * 9 / 5 + 32
            f = math.floor(f * 10) / 10

            pending = trainer.pending_experience_count()


            message = 'Current temperature is ' + str(f)

            if solenoid.isOn():
                message += '</br>Heater is running'
            else:
                message += '</br>Heater is not running'

            message += '</br>Pending experiences to send ' + str(pending)
        except (EOFError, Exception):
            pass

        return message

    def run(id):

        hostName = ''
        hostPort = 80

        webServer = HTTPServer((hostName, hostPort), WebServer)

        try:
            webServer.serve_forever()
        except KeyboardInterrupt:
            pass

        webServer.server_close()

webServerThread = Thread(target=WebServer.run, args=[0])
webServerThread.start()

while True:
    start = time.time()

    if Settings.getOn():

        if Settings.getGathering():
            trainer.run_once()

        if Settings.getTraining():
            trainer.send_experiences()

    elapse = time.time() - start

    # print(elapse)

    if elapse < 5:
        time.sleep(5 - elapse)
