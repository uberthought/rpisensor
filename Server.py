#!/usr/bin/python3

from threading import Thread
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import cgi
import math

from Communication import Communication
from Experiences import Experiences

enabled = True

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


    def showRoot(self, message):

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        with open('Server.html', 'r') as indexfile:
            self.wfile.write(bytes(indexfile.read(), 'utf-8'))

        self.wfile.write(bytes('<script>', 'utf-8'))
    
        self.wfile.write(bytes('document.getElementById("message").innerHTML = "' + message + '";', 'utf-8'))
    
        # self.wfile.write(bytes('document.getElementById("target").innerHTML = "' + str(Settings.getTargetF()) + '";', 'utf-8'))
    
        if enabled:
            self.wfile.write(bytes('document.getElementById("power").value = "Disable";', 'utf-8'))
        else:
            self.wfile.write(bytes('document.getElementById("power").value = "Enable";', 'utf-8'))
    
        self.wfile.write(bytes('</script>', 'utf-8'))

    def powerButton(self):
        global enabled
        enabled = not enabled
        self.showRoot(self.getState())

    def getState(self):
        experiences = Experiences()
        last = experiences.last()
        timestamp = last[4]
        if timestamp != None:
            timestamp = timestamp[0]
        message = str(experiences)
        message += '<br>'
        message += str(timestamp)
        return message

    def run(id):
        hostName = ''
        hostPort = 8080

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

    elapse = time.time() - start

    if enabled:
        communication = Communication()
        experiences = communication.receive('')
        experiences.append()

    # print(elapse)

    if elapse < 5:
        time.sleep(5 - elapse)
