'''OSC test'''
import argparse
import logging

from pythonosc import osc_message_builder
from pythonosc import udp_client

logger = logging.getLogger(__name__)


class OSCClient:
    def __init__(self, ip, port):
        self.client = udp_client.SimpleUDPClient(ip, port)

    def command(self, addr, arg_value=None, arg_type=None):
        logger.debug("command: %s %s" % (arg_value, arg_type))
        builder = osc_message_builder.OscMessageBuilder(addr)
        if arg_value != None:
            if type(arg_value) != str and getattr(arg_value, '__iter__', False):
                for arg in arg_value:
                    builder.add_arg(arg, arg_type)
            else:
                builder.add_arg(arg_value, arg_type)
        cmd = builder.build()
        logger.debug('osc send: %s %s' % (cmd.address, cmd.params))
        self.client.send(cmd)

    def pattern(self, num):
        self.command('/pattern', num)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--ip', default='127.0.0.1', help='The ip of the OSC server')
    parser.add_argument(
        '--port',
        type=int,
        default=5005,
        help='The port the OSC server is listening on')
    parser.add_argument(
        '--addr', default='/ping', help='OSC addr (default /ping)')
    parser.add_argument('--args', default='', help='OSC args')
    args = parser.parse_args()

    client = udp_client.SimpleUDPClient(args.ip, args.port)

    builder = osc_message_builder.OscMessageBuilder(args.addr)
    if args.args != '':
        builder.add_arg(args.args)

    client.send(builder.build())
