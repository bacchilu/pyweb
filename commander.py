#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
commander.py - https://github.com/bacchilu/pyweb

Cmd parser

Luca Bacchi <bacchilu@gmail.com> - http://www.lucabacchi.it
"""

import multiprocessing
import cmd

import web
import controller


class ServiceManager(object):

    q = multiprocessing.Queue()
    controllerFn = None

    @classmethod
    def start(cls, service):
        if service in ['all', '']:
            cls.start('web')
            cls.start('controller')
            return
        if service == 'web':
            web.WebServer.start(cls.q)
        if service == 'controller':
            controller.Consumer.start(cls.q, cls.controllerFn)

    @classmethod
    def stop(cls, service):
        if service in ['all', '']:
            cls.stop('web')
            cls.stop('controller')
            return
        if service == 'web':
            web.WebServer.stop()
        if service == 'controller':
            controller.Consumer.stop()

    @classmethod
    def status(cls, service):
        if service == 'web':
            web.WebServer.status()
        if service == 'controller':
            controller.Consumer.status()
        if service in ['all', '']:
            cls.status('web')
            cls.status('controller')


class Commander(cmd.Cmd):

    intro = 'help per una lista dei comandi'

    def __init__(self, controllerFn):
        cmd.Cmd.__init__(self)
        ServiceManager.controllerFn = staticmethod(controllerFn)

    def do_start(self, service):
        """start [service]
        Avvia tutti i servizi o un servizio
        service={web|controller}"""

        ServiceManager.start(service)
        self.do_status(service)

    def do_stop(self, service):
        """stop [service]
        Arresta tutti i servizi o un servizio
        service={web|controller}"""

        ServiceManager.stop(service)
        self.do_status(service)

    def do_status(self, service):
        """status [service]
        Info su un particolare servizio
        service={web|controller}"""

        ServiceManager.status(service)

    def do_restart(self, service):
        """stop [service]
        Arresta tutti i servizi o un servizio
        service={web|controller}"""

        self.do_stop(service)
        self.do_start(service)

    def do_exit(self, line):
        """Esce"""

        self.do_stop(line)
        return True


def start(controllerFn):
    Commander(controllerFn).cmdloop()


if __name__ == '__main__':


    def dummyFn(host, path):
        if path == '/crash':
            raise Exception('errore')


    start(dummyFn)
