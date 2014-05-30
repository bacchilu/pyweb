#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
server.py - https://github.com/bacchilu/pyweb

Elabora le richieste del web server

Luca Bacchi <bacchilu@gmail.com> - http://www.lucabacchi.it
"""

import multiprocessing


class Consumer(object):

    @classmethod
    def worker(cls):
        i = 1
        while True:
            item = cls.q.get()
            if item is None:
                return
            print i
            i += 1

    @classmethod
    def start(cls, q):
        cls.q = q
        cls.p = multiprocessing.Process(target=cls.worker)
        cls.p.start()

    @classmethod
    def stop(cls):
        cls.q.put(None)
        cls.p.join()


