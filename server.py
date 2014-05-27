#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
server.py - https://github.com/bacchilu/pyweb

http://code.activestate.com/recipes/425210-simple-stoppable-server-using-socket-timeout/

Luca Bacchi <bacchilu@gmail.com> - http://www.lucabacchi.it
"""

import BaseHTTPServer
import socket
import multiprocessing


class GetHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write('OK')
        self.wfile.close()

    def log_message(self, format, *args):
        import sys
        sys.stderr.write('%s - - [%s] %s\n' % (self.client_address[0],
                         self.log_date_time_string(), format % args))


class StoppableHTTPServer(BaseHTTPServer.HTTPServer):

    def server_bind(self):
        BaseHTTPServer.HTTPServer.server_bind(self)
        self.socket.settimeout(1)
        self.exit = multiprocessing.Event()

    def get_request(self):
        while not self.exit.is_set():
            try:
                (sock, addr) = self.socket.accept()
                sock.settimeout(None)
                return (sock, addr)
            except socket.timeout:
                pass

    def stop(self):
        self.exit.set()

    def serve(self):
        while not self.exit.is_set():
            self.handle_request()


class WebServer(object):

    @classmethod
    def start(cls):
        cls.httpd = StoppableHTTPServer(('127.0.0.1', 8080), GetHandler)
        cls.p = multiprocessing.Process(target=cls.httpd.serve)
        cls.p.start()

    @classmethod
    def stop(cls):
        cls.httpd.stop()
        cls.p.join()


if __name__ == '__main__':
    WebServer.start()
    raw_input('Press <RETURN> to stop server\n')
    WebServer.stop()
