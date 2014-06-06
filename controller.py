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
import traceback

import logger


def isParentAlive(parentPID):
    return os.getppid() == parentPID


class Consumer(object):

    p = None

    @classmethod
    def worker(cls, parentPID, actionFn):
        while not cls.exit.is_set() and isParentAlive(parentPID):
            try:
                (host, path) = cls.q.get(True, 1)
                logger.debug('Evaluating %s %s' % (host, path))
                actionFn(host, path)
            except Queue.Empty:

                pass
            except:
                logger.error(traceback.format_exc())

    @classmethod
    def start(cls, q, actionFn):
        if cls.p is not None and cls.p.is_alive():
            return

        cls.q = q
        cls.exit = multiprocessing.Event()
        cls.p = multiprocessing.Process(name='controller',
                target=cls.worker, args=(os.getpid(), actionFn))
        cls.p.daemon = True
        cls.p.start()
        logger.info('Avviato controller')

    @classmethod
    def stop(cls):
        if cls.p is None or not cls.p.is_alive():
            return

        cls.exit.set()
        cls.p.join()
        logger.info('Arrestato controller')

    @classmethod
    def status(cls):
        if cls.p is None or not cls.p.is_alive():
            print 'controller is down'
        else:
            print 'controller:', cls.p.pid


