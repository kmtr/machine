# -*- coding: utf-8 -*-
import logging
from machine import Machine
from osc_server import OSCServer, MachineDriver
try:
    import pigpio
except ImportError:
    import pigpio_mock as pigpio

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    pi = pigpio.pi()
    machine = Machine(pi)
    machine.setup()

    md = MachineDriver(machine)
    server = OSCServer(md)
    server.serve_forever()
