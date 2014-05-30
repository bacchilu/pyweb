#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
server.py - https://github.com/bacchilu/pyweb

Web server multiprocessing

Luca Bacchi <bacchilu@gmail.com> - http://www.lucabacchi.it
"""

import BaseHTTPServer
import socket
import multiprocessing


class GetHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_GET(self):
        self.server.cmdQueue.put(self.client_address[0])

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
        self.close = multiprocessing.Event()

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
        self.close.wait()
        self.server_close()

    def serve(self, q):
        self.cmdQueue = q
        while not self.exit.is_set():
            self.handle_request()
        self.cmdQueue.close()
        self.cmdQueue.join_thread()
        self.close.set()


class WebServer(object):

    @classmethod
    def start(cls, q):
        cls.httpd = StoppableHTTPServer(('127.0.0.1', 8080), GetHandler)
        cls.p = multiprocessing.Process(target=cls.httpd.serve,
                args=(q, ))
        cls.p.start()

    @classmethod
    def stop(cls):
        cls.httpd.stop()
        cls.p.join()


