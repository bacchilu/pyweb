#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
logger.py - https://github.com/bacchilu/pyweb

Il logger è in pratica un thread che attende i messaggi da loggare da una coda.
Non implemento nessun meccanismo particolarmente sofisticato per la chiusura del
thread: daemon=True.

Luca Bacchi <bacchilu@gmail.com> - http://www.lucabacchi.it
"""

import multiprocessing
import threading
import logging

FORMAT = \
    '%(asctime)s [pid %(process)5d|%(processName)-13s] %(levelname)-8s - %(message)s'
logging.basicConfig(filename='logger.log', level=logging.DEBUG,
                    format=FORMAT)


def loggerWorker(q):
    while True:
        (level, msg) = q.get()
        if level == 'debug':
            logging.debug(msg)


q = multiprocessing.Queue()
t = threading.Thread(target=loggerWorker, args=(q, ))
t.daemon = True
t.start()


def debug(msg):
    q.put(('debug', msg))


