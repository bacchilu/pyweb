#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
controller.py - https://github.com/bacchilu/pyweb

Elabora le richieste del web server
If the parent process seems not to be alive anymore, this process commits
suicide
(http://stackoverflow.com/questions/2542610/python-daemon-doesnt-kill-its-kids)

Luca Bacchi <bacchilu@gmail.com> - http://www.lucabacchi.it
"""

import multiprocessing
import Queue
import os

import logger


def isParentAlive(parentPID):
    return os.getppid() == parentPID


class Consumer(object):

    p = None

    @classmethod
    def worker(cls, parentPID):
        i = 1
        while not cls.exit.is_set() and isParentAlive(parentPID):
            try:
                item = cls.q.get(True, 1)
                if item is None:
                    return
                logger.debug('%d' % i)
                i += 1
            except Queue.Empty:
                pass

    @classmethod
    def start(cls, q):
        if cls.p is not None and cls.p.is_alive():
            return

        cls.q = q
        cls.exit = multiprocessing.Event()
        cls.p = multiprocessing.Process(name='controller',
                target=cls.worker, args=(os.getpid(), ))
        cls.p.daemon = True
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
            print 'controller is down'
        else:
            print 'controller:', cls.p.pid


