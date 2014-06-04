#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
server.py - https://github.com/bacchilu/pyweb

Elabora le richieste del web server

Luca Bacchi <bacchilu@gmail.com> - http://www.lucabacchi.it
"""

import multiprocessing
import Queue


class Consumer(object):

    p = None

    @classmethod
    def worker(cls):
        i = 1
        while not cls.exit.is_set():
            try:
                item = cls.q.get(True, 1)
                if item is None:
                    return
                print i
                i += 1
            except Queue.Empty:
                pass

    @classmethod
    def start(cls, q):
        if cls.p is not None and cls.p.is_alive():
            return

        cls.q = q
        cls.exit = multiprocessing.Event()
        cls.p = multiprocessing.Process(target=cls.worker)
        cls.p.start()
        print 'controller:', cls.p.pid

    @classmethod
    def stop(cls):
        if cls.p is None or not cls.p.is_alive():
            return

        cls.exit.set()
        cls.p.join()

    @classmethod
    def status(cls):
        if cls.p is None or not cls.p.is_alive():
            print 'controller is down'
        else:
            print 'controller:', cls.p.pid


