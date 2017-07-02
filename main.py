# -*- coding: utf-8 -*-
import argparse
import logging

from osc_server import OSCServer, MachineDriver

from machine import Machine
try:
    import pigpio
except ImportError:
    import mock as pigpio

if __name__ == '__main__':
    argsParser = argparse.ArgumentParser(prog='machine server')
    argsParser.add_argument('--ip',
                        default='127.0.0.1', help='The ip to listen on. (default 127.0.0.1')
    argsParser.add_argument('--port',
                        type=int, default=5005, help='The port to listen on. (default 5005)')
    argsParser.add_argument('--debug',
                        type=bool, default=False)

    args = argsParser.parse_args()
    print(args)
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    pi = pigpio.pi()
    machine = Machine(pi)
    machine.setup()

    md = MachineDriver(machine)
    server = OSCServer(md, ip=args.ip, port=args.port)
    server.serve_forever()
