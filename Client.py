#!/usr/bin/python3

from threading import Thread
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import datetime
import cgi
import math

from Settings import Settings
# from Sensor import Sensor
from Experiences import Experiences
from Communication import Communication

settings = Settings()
# sensor = Sensor()
experiences = Experiences('client_experiences')
experiences.load()
communication = Communication()

elapse = 0
send_message = ''
temperature, humidity, timestamp = 0, 0, datetime.datetime.now()
# if settings.on:
#     temperature, humidity, timestamp = sensor.gather()

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
        if b'less_collecting' in postvars.keys():
            settings.collection_rate = settings.collection_rate + 1
        if b'more_collecting' in postvars.keys():
            if settings.collection_rate >= 6:
                settings.collection_rate = settings.collection_rate - 1
            
        settings.save()
        self.showRoot(self.getState())

    def showRoot(self, message):

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        with open('Client.html', 'r') as indexfile:
            self.wfile.write(bytes(indexfile.read(), 'utf-8'))

        self.wfile.write(bytes('<script>', 'utf-8'))
        if settings.on:
            self.wfile.write(bytes('document.getElementById("power").value = "Turn Off";', 'utf-8'))
        else:
            self.wfile.write(bytes('document.getElementById("power").value = "Turn On";', 'utf-8'))
        self.wfile.write(bytes('document.getElementById("collection_rate").innerHTML = "' + str(settings.collection_rate) + 's";', 'utf-8'))
        self.wfile.write(bytes('document.getElementById("message").innerHTML = "' + message + '";', 'utf-8'))
        self.wfile.write(bytes('</script>', 'utf-8'))

    def getState(self):
        message = ''

        try:
            if settings.on:
                f = temperature * 9 / 5 + 32
                f = math.floor(f * 10) / 10

                message = 'Temperature ' + str(f) + "F"
                message += '</br>Humidity ' + str(humidity) + "%"
                message += '</br>Timestamp ' + str(timestamp)
                message += '</br>'
                message += '</br>Experiences ' + str(len(experiences.temperatures))
                message += '</br>Elapsed ' + str(elapse) + "s"
                message += '</br>Sending ' + send_message

            else:
                message = "Not recording"
            
        except (EOFError, Exception) as e:
            message = e.strerror
            pass

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

    if settings.on:
        # temperature, humidity, timestamp = sensor.gather()
        experiences.add(temperature, humidity, timestamp)
        experiences.save()
        experiences.saveCSV()

        if len(experiences.timestamps) > 1:
            try:
                communication = Communication()
                communication.send('localhost', experiences)
                send_message = 'Sent ' + str(len(experiences.timestamps))
                experiences.reset()
                experiences.save()
            except (ConnectionRefusedError, ConnectionResetError) as e:
                send_message = e.strerror

    elapse = time.time() - start

    if elapse < settings.collection_rate:
        time.sleep(settings.collection_rate - elapse)
