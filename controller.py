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
        cls.q = q
        cls.exit = multiprocessing.Event()
        cls.p = multiprocessing.Process(target=cls.worker)
        cls.p.start()

    @classmethod
    def stop(cls):
        cls.exit.set()
        cls.p.join()


