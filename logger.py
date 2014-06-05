#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
logger.py - https://github.com/bacchilu/pyweb

Luca Bacchi <bacchilu@gmail.com> - http://www.lucabacchi.it
"""

import multiprocessing
import logging

FORMAT = \
    '%(asctime)s [pid %(process)5d|%(processName)-13s] %(levelname)-8s - %(message)s'
logging.basicConfig(filename='logger.log', level=logging.DEBUG,
                    format=FORMAT)


def debug(msg):
    logging.debug(msg)


