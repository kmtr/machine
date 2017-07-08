# -*- coding: utf-8 -*-
import argparse
import logging

from osc_server import OSCServer, MachineDriver

from machine import Machine
import pigpio_provider

if __name__ == '__main__':
    argsParser = argparse.ArgumentParser(prog='machine server')
    argsParser.add_argument(
        '--ip',
        default='127.0.0.1',
        help='The ip to listen on. (default 127.0.0.1')
    argsParser.add_argument(
        '--port',
        type=int,
        default=5005,
        help='The port to listen on. (default 5005)')
    argsParser.add_argument('--debug', type=bool, default=False)

    args = argsParser.parse_args()
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    pi = pigpio_provider.pi()
    machine = Machine(pi)
    machine.setup()

    md = MachineDriver(machine)
    server = OSCServer(md, ip=args.ip, port=args.port)
    server.serve_forever()
