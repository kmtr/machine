'''osc server'''
# -*- coding: utf-8 -*-
import logging
import signal

from pythonosc import dispatcher
from pythonosc import osc_server

logger = logging.getLogger(__name__)


class OSCServer:

    def __init__(self, driver, ip='127.0.0.1', port=5005):
        self._server = osc_server.ThreadingOSCUDPServer(
            (ip, port), driver.dispatcher)
        self._driver = driver

        def sigint_func(_num, _frame):
            '''sigint_func catch SIGINT and close osc server'''
            self.close()
            if hasattr(self._driver, 'close'):
                self._driver.close()
            exit()
        signal.signal(signal.SIGINT, sigint_func)

    def serve_forever(self):
        '''server start and listen client'''
        logger.info("Start serving on %s", self._server.server_address)
        self._server.serve_forever()

    def close(self):
        '''close server'''
        logger.info("Stop serving on %s", self._server.server_address)
        self._server.server_close()


class MachineDriver:

    def __init__(self, machine):
        self.dispatcher = dispatcher.Dispatcher()
        self.dispatcher.map('/ping', self.pong_dispatcher)
        self.dispatcher.map('/servo', self.servo_dispatcher)
        self.dispatcher.set_default_handler(self.wild_card_dispatcher)
        self.machine = machine

    def __debug(self, addr, *args):
        logger.debug('{} {}'.format(addr, args))

    def wild_card_dispatcher(self, addr, *args):
        logger.warn('unknown addr: {} {}'.format(addr, args))

    def pong_dispatcher(self, unused_addr, *args):
        '''pong_dispatcher for checking status'''
        print('pong')

    def servo_dispatcher(self, addr, *args):
        self.__debug(addr, *args)
        for arg in args[:8]:
            print(addr, arg)

    def close(self):
        logger.info('close machine')
        self.machine.close()


if __name__ == '__main__':
    machineDriver = MachineDriver(None)
    server = OSCServer(machineDriver)
    server.serve_forever()
