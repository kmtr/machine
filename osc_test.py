'''OSC test'''
import argparse

from pythonosc import osc_message_builder
from pythonosc import udp_client


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', default='127.0.0.1',
                        help='The ip of the OSC server')
    parser.add_argument('--port', type=int, default=5005,
                        help='The port the OSC server is listening on')
    parser.add_argument('--addr', default='/ping',
                        help='OSC addr (default /ping)')
    parser.add_argument('--args', default='',
                        help='OSC args')
    args = parser.parse_args()

    client = udp_client.SimpleUDPClient(args.ip, args.port)

    builder = osc_message_builder.OscMessageBuilder(args.addr)
    if args.args != '':
        builder.add_arg(args.args)

    client.send(builder.build())
