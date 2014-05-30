#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
server.py - https://github.com/bacchilu/pyweb

http://code.activestate.com/recipes/425210-simple-stoppable-server-using-socket-timeout/

Luca Bacchi <bacchilu@gmail.com> - http://www.lucabacchi.it
"""

import multiprocessing

import web
import controller

if __name__ == '__main__':
    q = multiprocessing.Queue()

    web.WebServer.start(q)
    controller.Consumer.start(q)

    raw_input('Press <RETURN> to stop server\n')

    web.WebServer.stop()
    controller.Consumer.stop()

    q.close()
    q.join_thread()
