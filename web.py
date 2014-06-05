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


class WebServerProcess(multiprocessing.Process):

    def __init__(self, q):
        multiprocessing.Process.__init__(self)
        self.httpd = StoppableHTTPServer(('127.0.0.1', 8080),
                GetHandler)
        self.q = q

    def run(self):
        self.httpd.serve(self.q)

    def stop(self):
        self.httpd.stop()


class WebServer(object):

    p = None

    @classmethod
    def start(cls, q):
        if cls.p is not None and cls.p.is_alive():
            return

        cls.p = WebServerProcess(q)
        cls.p.start()

    @classmethod
    def stop(cls):
        if cls.p is None or not cls.p.is_alive():
            return

        cls.p.stop()
        cls.p.join()

    @classmethod
    def status(cls):
        if cls.p is None or not cls.p.is_alive():
            print 'web is down'
        else:
            print 'web:', cls.p.pid


