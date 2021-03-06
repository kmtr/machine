'''osc server'''
# -*- coding: utf-8 -*-
import logging
import signal

from machine import Machine
from pythonosc import dispatcher
from pythonosc import osc_server

from patterns import Pattern, PATTERNS, PATTERN_RESET

logger = logging.getLogger(__name__)


class OSCServer:
    def __init__(self, driver, ip='127.0.0.1', port=5005):
        self._server = osc_server.ThreadingOSCUDPServer((ip, port),
                                                        driver.dispatcher)
        self._driver = driver

        def sigint_func(_num, _frame):
            '''sigint_func catch SIGINT and close osc server'''
            self.close()
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
        self._driver.close()


class MachineDriver:
    def __init__(self, machine: Machine):
        self.dispatcher = dispatcher.Dispatcher()
        self.dispatcher.map('/ping', self.pong_dispatcher)
        self.dispatcher.map('/reset', self.reset_dispatcher)
        self.dispatcher.map('/pattern', self.pattern_dispatcher)
        self.dispatcher.map('/set', self.servo_degree_dispatcher)
        self.dispatcher.set_default_handler(self.wild_card_dispatcher)
        self.machine = machine

    def __debug(self, addr, *args):
        logger.debug('%s %s' % (addr, args))

    def wild_card_dispatcher(self, addr, *args):
        logger.warn('unknown addr: %s %s' % (addr, args))

    def pong_dispatcher(self, unused_addr, *args):
        '''pong_dispatcher for checking status'''
        print('pong')

    def reset_dispatcher(self, addr, *args):
        try:
            self.machine.set_servo_degree_pattern(PATTERN_RESET)
        except Exception as ex:
            logger.error(ex)

    def servo_degree_dispatcher(self, addr, *args):
        self.__debug(addr, *args)
        try:
            key = args[0]
            degree = args[1]
            self.machine.set_servo_degree(key, degree)
        except Exception as ex:
            logger.error(ex)

    def pattern_dispatcher(self, addr, val):
        if val in PATTERNS:
            pattern = PATTERNS[val]
            try:
                self.machine.set_servo_degree_pattern(pattern)
            except Exception as ex:
                logger.error(ex)
        else:
            logger.warn('%s key is not in PATTERNS' % val)

    def close(self):
        logger.info('close machine')
        if hasattr(self.machine, 'close'):
            self.machine.close()


if __name__ == '__main__':
    machineDriver = MachineDriver(None)
    server = OSCServer(machineDriver)
    server.serve_forever()
