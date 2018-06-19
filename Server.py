#!/usr/bin/python3

from threading import Thread
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import cgi
import math

from Communication import Communication
from Experiences import Experiences
from Settings import Settings

settings = Settings()

elapse = 0
receive_message = ''

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
            settings.on = not settings.on

    def showRoot(self, message):

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        with open('Server.html', 'r') as indexfile:
            self.wfile.write(bytes(indexfile.read(), 'utf-8'))

        self.wfile.write(bytes('<script>', 'utf-8'))
        if settings.on:
            self.wfile.write(bytes('document.getElementById("power").value = "Turn Off";', 'utf-8'))
        else:
            self.wfile.write(bytes('document.getElementById("power").value = "Turn On";', 'utf-8'))
        self.wfile.write(bytes('document.getElementById("message").innerHTML = "' + message + '";', 'utf-8'))
        self.wfile.write(bytes('</script>', 'utf-8'))

    def getState(self):
        global receive_message
        global elapse

        experiences = Experiences('server_experiences')
        experiences.load()
        count = len(experiences.timestamps)
        message = 'Collected ' + str(count) + ' experiences.'
        if count > 0:
            timestamp = experiences.timestamps[-1]
            message += '<br>'
            message += 'Last experience was ' + timestamp.strftime('%H:%M:%S') + "(UTC)"
            message += '</br>'
            message += '</br>Experiences ' + str(len(experiences.temperatures))
            message += '</br>Elapsed ' + str(elapse) + "s"
            message += '</br>Receiving ' + receive_message

        return message

    def run():
        hostName = ''
        hostPort = 8081

        webServer = HTTPServer((hostName, hostPort), WebServer)

        try:
            webServer.serve_forever()
        except KeyboardInterrupt:
            pass

        webServer.server_close()

def runCommunications():
    global receive_message
    global elapse
    
    communication = Communication()

    while True:
        start = time.time()

        if settings.on:
            try:
                experiences2 = communication.receive('')
                count = len(experiences2.timestamps)
                experiences2.append('server_experiences')
                receive_message = 'Received ' + str(count)
            except (ConnectionRefusedError, ConnectionResetError) as e:
                receive_message = e.strerror
        else:
            receive_message = ''
            time.sleep(.1)

        elapse = time.time() - start

    
webServerThread = Thread(target=WebServer.run)
webServerThread.start()

communicationsThread = Thread(target=runCommunications)
communicationsThread.start()