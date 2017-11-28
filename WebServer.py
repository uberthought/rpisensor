#!/usr/bin/python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import cgi
import logging

from Settings import Settings

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

#hostName = "ec2-13-58-202-229.us-east-2.compute.amazonaws.com"
hostName = ''
hostPort = 80

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

        logger.debug('TYPE %s' % (ctype))
        logger.debug('PATH %s' % (self.path))
        logger.debug('ARGS %d' % (len(postvars)))

        print(postvars)

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

        settings = Settings()

        self.wfile.write(bytes('<script>', 'utf-8'))
        self.wfile.write(bytes('document.getElementById("message").innerHTML ="' + message + '";', 'utf-8'))
        self.wfile.write(bytes('document.getElementById("target").innerHTML ="' + str(settings.getTargetF()) + '";', 'utf-8'))
        if settings.getOn():
            self.wfile.write(bytes('document.getElementById("power").value ="Turn Off";', 'utf-8'))
        else:
            self.wfile.write(bytes('document.getElementById("power").value ="Turn On";', 'utf-8'))
        self.wfile.write(bytes('</script>', 'utf-8'))

    def warmerButton(self):
        logger.debug('warmerButton')
        settings = Settings()
        settings.setTargetF(settings.getTargetF() + 1)
        self.showRoot(self.getState())

    def coolerButton(self):
        logger.debug('coolerButton')
        settings = Settings()
        settings.setTargetF(settings.getTargetF() - 1)
        self.showRoot(self.getState())

    def powerButton(self):
        logger.debug('powerButton')
        settings = Settings()
        settings.setOn(not settings.getOn())
        self.showRoot(self.getState())

    def getState(self):
        settings = Settings()
        message = 'Heater is '
        if settings.getOn():
            message += 'on'
        else:
            message += 'off'
        
        # message += '</br>Current temperature is ' + str(settings.getTargetF())
        
        return message

webServer = HTTPServer((hostName, hostPort), WebServer)

try:
    webServer.serve_forever()
except KeyboardInterrupt:
    pass

webServer.server_close()
logger.info(time.asctime() + "Server Stops - %s:%s" % (hostName, hostPort))


