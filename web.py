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
import logging


class GetHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_GET(self):
        self.server.cmdQueue.put(self.client_address[0])

        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write('OK')
        self.wfile.close()

    def log_message(self, fmt, *args):
        name = multiprocessing.current_process().name
        msg = '%s - - [%s] %s' % (self.client_address[0],
                                  self.log_date_time_string(), fmt
                                  % args)
        logging.debug(':%s -> %s' % (name, msg))


class StoppableHTTPServer(BaseHTTPServer.HTTPServer):

    def server_bind(self):
        BaseHTTPServer.HTTPServer.server_bind(self)
        self.socket.settimeout(1)

    def get_request(self):
        while not self.exit.is_set():
            try:
                (sock, addr) = self.socket.accept()
                sock.settimeout(None)
                return (sock, addr)
            except socket.timeout:
                pass

    def serve(self, q):
        self.cmdQueue = q
        while not self.exit.is_set():
            self.handle_request()
        self.cmdQueue.close()
        self.cmdQueue.join_thread()


class WebServer(object):

    p = None

    @classmethod
    def worker(cls, exit, q):
        httpd = StoppableHTTPServer(('127.0.0.1', 8080), GetHandler)
        httpd.exit = exit
        httpd.serve(q)

    @classmethod
    def start(cls, q):
        if cls.p is not None and cls.p.is_alive():
            return

        cls.exit = multiprocessing.Event()
        cls.p = multiprocessing.Process(name='web', target=cls.worker,
                args=(cls.exit, q))
        cls.p.start()

    @classmethod
    def stop(cls):
        if cls.p is None or not cls.p.is_alive():
            return

        cls.exit.set()
        cls.p.join()

    @classmethod
    def status(cls):
        if cls.p is None or not cls.p.is_alive():
            print 'web is down'
        else:
            print 'web:', cls.p.pid


