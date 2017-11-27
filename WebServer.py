#!/usr/bin/python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import cgi
import logging

#hostName = "ec2-13-58-202-229.us-east-2.compute.amazonaws.com"
hostName = ''
hostPort = 9000

class WebServer(BaseHTTPRequestHandler):


    def do_GET(self):

        self.show_root('')

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

        if b'Test' in postvars:
            self.test_button()
        else:
            self.show_root()


    def show_root(self, message):

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>Title.</title></head>", "utf-8"))

        self.wfile.write(bytes("<body><p>This is a test.</p>", "utf-8"))

        self.wfile.write(bytes("<form action = \"\" method = \"post\">", "utf-8"))
        self.wfile.write(bytes("<input type=\"submit\" name=\"Test\" value=\"Test\" />", "utf-8"))
        self.wfile.write(bytes("</form>", "utf-8"))

        self.wfile.write(bytes(message, "utf-8"))

        self.wfile.write(bytes("</body></html>", "utf-8"))


    def test_button(self):

        logging.debug('test_button()')

        test = Test()
        test_result = test.run()

        self.show_root(test_result)


webServer = HTTPServer((hostName, hostPort), WebServer)

try:
    webServer.serve_forever()
except KeyboardInterrupt:
    pass

webServer.server_close()
logging.info(time.asctime() + "Server Stops - %s:%s" % (hostName, hostPort))


