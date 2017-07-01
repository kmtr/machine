# -*- coding: utf-8 -*-
from machine import Machine
from osc_server import OSCServer, MachineDriver
try:
    import pigpio
except ImportError:
    import pigpio_mock as pigpio

if __name__ == '__main__':
    pi = pigpio.pi()
    machine = Machine(pi)
    machine.setup()

    md = MachineDriver(machine)
    server = OSCServer(md)
    server.serve_forever()

    pi.stop()