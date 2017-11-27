#!/usr/bin/python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import cgi
import logging

from Settings import Settings

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

        logging.debug('TYPE %s' % (ctype))
        logging.debug('PATH %s' % (self.path))
        logging.debug('ARGS %d' % (len(postvars)))

        print(postvars)

        if b'save' in postvars.keys():
            # self.showRoot('tapped save')
            self.saveButton(postvars)
        else:
            self.showRoot('unknown error')


    def showRoot(self, message):

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        with open('WebServer/index.html', 'r') as indexfile:
            self.wfile.write(bytes(indexfile.read(), 'utf-8'))

        settings = Settings()

        self.wfile.write(bytes('<script>', 'utf-8'))
        self.wfile.write(bytes('document.getElementById("message").innerHTML ="' + message + '";', 'utf-8'))
        self.wfile.write(bytes('document.getElementById("target").value ="' + str(settings.getTargetF()) + '";', 'utf-8'))
        if settings.getOn():
            self.wfile.write(bytes('document.getElementById("on").checked = true;', 'utf-8'))
        else:
            self.wfile.write(bytes('document.getElementById("on").checked = false;', 'utf-8'))
        self.wfile.write(bytes('</script>', 'utf-8'))

    def saveButton(self, postvars):

        logging.debug('saveButton')

        settings = Settings()

        if b'on' in postvars.keys():
            settings.setOn(True)
        else:
            settings.setOn(False)

        for item in postvars.items():
            if item[0] == b'target':
                target = (item[1][0]).decode("utf-8")
                settings.setTargetF(target)

        self.showRoot(self.getState())
    
    def getState(self):
        settings = Settings()
        message = 'Heater is '
        if settings.getOn():
            message += 'on'
        else:
            message += 'off'
        
        message += '</br>Target temperature is ' + str(settings.getTargetF())
        
        return message


webServer = HTTPServer((hostName, hostPort), WebServer)

try:
    webServer.serve_forever()
except KeyboardInterrupt:
    pass

webServer.server_close()
logging.info(time.asctime() + "Server Stops - %s:%s" % (hostName, hostPort))


