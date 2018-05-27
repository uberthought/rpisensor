#!/usr/bin/python3

from threading import Thread
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import cgi
import math

from Communication import Communication
from Experiences import Experiences
from Settings import Settings
from network import Model

model_loss = math.inf
dqn_loss = math.inf

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

        if b'power' in postvars.keys():
            self.powerButton()
        if b'training' in postvars.keys():
            self.trainingButton()

    def showRoot(self, message):

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        with open('Server.html', 'r') as indexfile:
            self.wfile.write(bytes(indexfile.read(), 'utf-8'))

        self.wfile.write(bytes('<script>', 'utf-8'))
    
        self.wfile.write(bytes('document.getElementById("message").innerHTML = "' + message + '";', 'utf-8'))
    
        # self.wfile.write(bytes('document.getElementById("target").innerHTML = "' + str(Settings.getTargetF()) + '";', 'utf-8'))

        if Settings.getTraining():
            self.wfile.write(bytes('document.getElementById("training").value = "Stop Training";', 'utf-8'))
        else:
            self.wfile.write(bytes('document.getElementById("training").value = "Start Training";', 'utf-8'))
    
        if Settings.getOn():
            self.wfile.write(bytes('document.getElementById("power").value = "Disable";', 'utf-8'))
            # self.wfile.write(bytes('document.getElementById("gathering").disabled = false;', 'utf-8'))
        else:
            self.wfile.write(bytes('document.getElementById("power").value = "Enable";', 'utf-8'))
            # self.wfile.write(bytes('document.getElementById("gathering").disabled = true;', 'utf-8'))
    
        self.wfile.write(bytes('</script>', 'utf-8'))

    def powerButton(self):
        Settings.setOn(not Settings.getOn())
        self.showRoot(self.getState())

    def trainingButton(self):
        Settings.setTraining(not Settings.getTraining())
        self.showRoot(self.getState())

    def getState(self):
        experiences = Experiences()
        count = len(experiences.timestamps)
        message = 'Collected ' + str(count) + ' experiences.'
        if count > 0:
            timestamp = experiences.timestamps[-1]
            message += '<br>'
            message += 'Last experience was ' + timestamp.strftime('%H:%M:%S') + "(UTC)"

        if model_loss != math.inf:
            message += '<br>'
            message += 'Last model loss ' + str(model_loss)

        if dqn_loss != math.inf:
            message += '<br>'
            message += 'Last dqn loss ' + str(dqn_loss)
            
        return message

    def run():
        hostName = ''
        hostPort = 8080

        webServer = HTTPServer((hostName, hostPort), WebServer)

        try:
            webServer.serve_forever()
        except KeyboardInterrupt:
            pass

        webServer.server_close()

def runCommunications():
    while True:
        start = time.time()

        if Settings.getOn():
            communication = Communication()
            experiences = communication.receive('')
            experiences.append()
            elapse = time.time() - start
            print(elapse)
        else:
            time.sleep(1)


def runTraining():

    global model_loss
    global dqn_loss

    model = Model()
    
    while True:

        if not Settings.getOn() or not Settings.getTraining():
            time.sleep(1)
            continue

        start = time.time()

        experiences = Experiences()
        model_loss = model.model_train(experiences, False)
        print('model', model_loss)

        dqn_loss = model.dqn_train(experiences, False)
        print('dqn', dqn_loss)

        model.save()

        elapse = time.time() - start
        print(elapse)
    
webServerThread = Thread(target=WebServer.run)
webServerThread.start()

communicationsThread = Thread(target=runCommunications)
communicationsThread.start()

trainingThread = Thread(target=runTraining)
trainingThread.start()

