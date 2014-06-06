#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
import threading


def worker():
    urllib2.urlopen('http://localhost:8080').read()


if __name__ == '__main__':
    for i in xrange(1024):
        threading.Thread(target=worker).start()
    print 'Partiti...'

