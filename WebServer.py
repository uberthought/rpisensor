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
        if b'warmer' in postvars.keys():
            self.warmerButton()
        if b'cooler' in postvars.keys():
            self.coolerButton()
        if b'power' in postvars.keys():
            self.powerButton()


    def showRoot(self, message):

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        with open('WebServer/index.html', 'r') as indexfile:
            self.wfile.write(bytes(indexfile.read(), 'utf-8'))

        self.wfile.write(bytes('<script>', 'utf-8'))
    
        self.wfile.write(bytes('document.getElementById("message").innerHTML ="' + message + '";', 'utf-8'))
    
        self.wfile.write(bytes('document.getElementById("target").innerHTML ="' + str(Settings.getTargetF()) + '";', 'utf-8'))
    
        if Settings.getGathering():
            self.wfile.write(bytes('document.getElementById("gathering").value ="Stop Gathering";', 'utf-8'))
        else:
            self.wfile.write(bytes('document.getElementById("gathering").value ="Start Gathering";', 'utf-8'))
    
        if Settings.getOn():
            self.wfile.write(bytes('document.getElementById("power").value ="Turn Off";', 'utf-8'))
        else:
            self.wfile.write(bytes('document.getElementById("power").value ="Turn On";', 'utf-8'))
    
        self.wfile.write(bytes('</script>', 'utf-8'))

    def warmerButton(self):
        Settings.setTargetF(Settings.getTargetF() + 1)
        self.showRoot(self.getState())

    def coolerButton(self):
        Settings.setTargetF(Settings.getTargetF() - 1)
        self.showRoot(self.getState())

    def powerButton(self):
        Settings.setOn(not Settings.getOn())
        if not Settings.getOn():
            solenoid = Solenoid()
            solenoid.switchOff()

        self.showRoot(self.getState())

    def gatheringButton(self):
        Settings.setGathering(not Settings.getGathering())
        self.showRoot(self.getState())

    def getState(self):
        sensor = Sensor()
        solenoid = Solenoid()
        temperature, _, _, _ = sensor.gather()
        f = temperature * 9 / 5 + 32
        f = math.floor(f * 10) / 10
        message = 'Current temperature is ' + str(f)

        if solenoid.isOn():
            message += '</br>Heater is running'
        else:
            message += '</br>Heater is not running'

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

trainer = OnlineTrainer()

while True:
    if Settings.getGathering():
        trainer.run_once()
    time.sleep(1)
