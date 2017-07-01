'''osc server'''
# -*- coding: utf-8 -*-
import logging
import signal

from pythonosc import dispatcher
from pythonosc import osc_server

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger('main')

class OSCServer:

    def __init__(self, driver, ip='127.0.0.1', port=5005):
        self._server = osc_server.ThreadingOSCUDPServer((ip, port), driver.dispatcher)
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
        LOGGER.info("Start serving on %s", self._server.server_address)
        self._server.serve_forever()

    def close(self):
        '''close server'''
        LOGGER.info("Stop serving on %s", self._server.server_address)
        self._server.server_close()


class MachineDriver:

    def __init__(self, machine):
        self.dispatcher = dispatcher.Dispatcher()
        self.dispatcher.map('/ping', self.pong_dispatcher)
        self.machine = machine

    def pong_dispatcher(self, unused_addr, args):
        '''pong_dispatcher for checking status'''
        print('pong')

    def close(self):
        LOGGER.info('close machine pigpiopi')
        self.machine.pigpiopi.stop()


if __name__ == '__main__':
    machineDriver = MachineDriver(None)
    server = OSCServer(machineDriver)
    server.serve_forever()