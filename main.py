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
import logger


class ServiceManager(object):

    q = multiprocessing.Queue()

    @classmethod
    def start(cls, service):
        if service in ['all', '']:
            cls.start('web')
            cls.start('controller')
            return
        if service == 'web':
            web.WebServer.start(cls.q)
        if service == 'controller':
            controller.Consumer.start(cls.q)
        logger.debug('Avviato %s' % service)

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
        logger.debug('Arrestato %s' % service)

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


if __name__ == '__main__':
    print 'help per una lista dei comandi'
    Commander().cmdloop()
