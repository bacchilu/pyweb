#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
server.py - https://github.com/bacchilu/pyweb

http://code.activestate.com/recipes/425210-simple-stoppable-server-using-socket-timeout/

Luca Bacchi <bacchilu@gmail.com> - http://www.lucabacchi.it
"""

import multiprocessing
import cmd

import web
import controller


class ServiceManager(object):

    @classmethod
    def startAll(cls):
        cls.q = multiprocessing.Queue()
        web.WebServer.start(cls.q)
        controller.Consumer.start(cls.q)

    @classmethod
    def stopAll(cls):
        web.WebServer.stop()
        controller.Consumer.stop()
        cls.q.close()
        cls.q.join_thread()


class Commander(cmd.Cmd):

    def do_start(self, service):
        """start [service]
        Avvia tutti i servizi o un servizio
        service={web|controller}"""

        ServiceManager.startAll()

    def do_stop(self, line):
        """stop [service]
        Arresta tutti i servizi o un servizio"""

        ServiceManager.stopAll()

    def do_exit(self, line):
        """Esce"""

        return True


if __name__ == '__main__':
    print 'help per una lista dei comandi'
    Commander().cmdloop()
