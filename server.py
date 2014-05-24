#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
server.py - https://github.com/bacchilu/pyweb

http://code.activestate.com/recipes/425210-simple-stoppable-server-using-socket-timeout/

Luca Bacchi <bacchilu@gmail.com> - http://www.lucabacchi.it
"""

import BaseHTTPServer
import socket
import threading


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write('OK')
        self.wfile.close()


class StoppableHTTPServer(BaseHTTPServer.HTTPServer):

    def server_bind(self):
        BaseHTTPServer.HTTPServer.server_bind(self)
        self.socket.settimeout(1)
        self.run = True

    def get_request(self):
        while self.run:
            try:
                (sock, addr) = self.socket.accept()
                sock.settimeout(None)
                return (sock, addr)
            except socket.timeout:
                pass

    def stop(self):
        self.run = False

    def serve(self):
        while self.run:
            self.handle_request()


if __name__ == '__main__':
    httpd = StoppableHTTPServer(('127.0.0.1', 8081), MyHandler)
    threading.Thread(target=httpd.serve).start()
    raw_input('Press <RETURN> to stop server\n')
    httpd.stop()
