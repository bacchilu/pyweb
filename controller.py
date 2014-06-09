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


class Pool(object):

    def __init__(self, initializer=None, initargs=None):
        self.workers = [multiprocessing.Process(name='PoolWorker-%d'
                        % (i + 1), target=initializer, args=initargs)
                        for i in range(multiprocessing.cpu_count())]
        for w in self.workers:
            w.daemon = True

    def start(self):
        for w in self.workers:
            w.start()

    def join(self):
        for w in self.workers:
            w.join()

    def status(self):
        return [p.pid for p in self.workers if p.is_alive()]

    def is_alive(self):
        return len(self.status()) != 0


class Consumer(object):

    pool = None

    @classmethod
    def worker(cls, parentPID, actionFn):
        logger.debug('Avviato %s'
                     % multiprocessing.current_process().name)
        while not cls.exit.is_set() and isParentAlive(parentPID):
            try:
                (host, path) = cls.q.get(True, 1)
                logger.debug('Evaluating %s %s' % (host, path))
                actionFn(host, path)
            except Queue.Empty:
                pass
            except:
                logger.error(traceback.format_exc())
        logger.debug('Terminato %s'
                     % multiprocessing.current_process().name)

    @classmethod
    def start(cls, q, actionFn):
        if cls.pool is not None and cls.pool.is_alive():
            return

        cls.q = q
        cls.exit = multiprocessing.Event()
        cls.pool = Pool(initializer=cls.worker, initargs=(os.getpid(),
                        actionFn))
        cls.pool.start()
        logger.info('Avviato controller')

    @classmethod
    def stop(cls):
        if cls.pool is None or not cls.pool.is_alive():
            return

        cls.exit.set()
        cls.pool.join()
        cls.pool = None
        logger.info('Arrestato controller')

    @classmethod
    def status(cls):
        if cls.pool is None or not cls.pool.is_alive():
            print 'controller is down'
        else:
            print 'controller:', cls.pool.status()


