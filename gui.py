'''machine view'''
# -*- coding: utf-8 -*-
import logging
import pickle
import threading
import tkinter
import turtle

from machine import Machine
from osc_client import OSCClient
from osc_server import MachineDriver, OSCServer
import pigpio_provider

logger = logging.getLogger(__name__)


def bind_event_data(widget, sequence, func, add=None):
    def _substitute(*args):
        e = lambda: None  #simplest object with __dict__
        e.data = eval(args[0])
        e.data['args'] = pickle.loads(e.data['args'])
        e.widget = widget
        return (e, )

    funcid = widget._register(func, _substitute, needcleanup=1)
    cmd = '{0}if {{"[{1} %d]" == "break"}} break\n'.format(
        '+' if add else '', funcid)
    widget.tk.call('bind', widget._w, sequence, cmd)


class Stub:

    eventPIGPIO = '<<PIGPIO>>'

    def __getattr__(self, attr):
        if hasattr(self.machine, attr):

            def wrapper(*args, **kw):
                pickled = pickle.dumps(args)
                self.root.event_generate(
                    Stub.eventPIGPIO, data={'args': pickled})
                return getattr(self.machine, attr)(*args, **kw)

            return wrapper
        raise AttributeError(attr)

    def __init__(self, ip: str, port: int):
        self.client = OSCClient(ip, port)

        self.root = tkinter.Tk()
        self.root.geometry("400x400")
        self.root.protocol("WM_DELETE_WINDOW", self.handleQuit)
        bind_event_data(self.root, Stub.eventPIGPIO, self.handlePIGPIO)

        self.canvas = tkinter.Canvas(self.root, width=400, height=400)
        self.screen = turtle.TurtleScreen(self.canvas)
        self.screen.tracer(0, 0)
        self.machine = Machine(pigpio_provider.pi('GUI', self.screen))
        self.machine.setup()

        frame_top = tkinter.Frame(self.root)
        self.button_ping = tkinter.Button(
            frame_top, text='ping', command=self.call_ping)
        self.button_reset = tkinter.Button(
            frame_top, text='reset', command=self.call_reset)
        self.button_ping.pack(side='left', anchor='n')
        self.button_reset.pack(side='left', anchor='n')

        frame_command = self.__renderFrameCommand()

        frame_top.pack()
        frame_command.pack()

        self.canvas.pack(anchor='s')

    def __renderFrameCommand(self):
        frame_command = tkinter.Frame(self.root)
        frame_entry_addr = tkinter.Frame(frame_command)
        self.label_addr = tkinter.Label(frame_entry_addr, text='/addr')
        self.entry_addr = tkinter.Entry(frame_entry_addr)
        self.entry_addr.insert(tkinter.END, '/pattern')
        self.entry_addr.bind('<Return>', func=lambda a: self.call_command())
        self.label_addr.pack(side='left', anchor='w')
        self.entry_addr.pack(side='left', anchor='w')
        frame_entry_addr.pack()

        frame_entry_args = tkinter.Frame(frame_command)
        self.label_args = tkinter.Label(frame_entry_args, text='args')
        self.entry_args = tkinter.Entry(frame_entry_args)
        self.entry_args.focus()
        self.entry_args.insert(tkinter.END, 1)
        self.entry_args.bind('<Return>', func=lambda a: self.call_command())

        self.label_args.pack(side='left', anchor='w')
        self.entry_args.pack(side='left', anchor='w')
        frame_entry_args.pack()

        self.button_command = tkinter.Button(
            frame_command, text='command', command=lambda: self.call_command())
        self.button_command.pack()
        return frame_command

    def setup(self, server: OSCServer):
        self.server = server
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.setDaemon(True)

    def loop(self):
        self.root.after(100, self.loop)

    def start(self):
        self.root.after(300, self.server_thread.start)
        self.root.after(400, self.loop)
        self.root.mainloop()

    def close(self):
        self.machine.close()

    def call_ping(self):
        self.client.command('/ping')

    def call_reset(self):
        self.client.command('/reset')

    def call_pattern(self, num):
        self.client.pattern(num)

    def call_command(self):
        addr = self.entry_addr.get()
        if addr == '':
            return
        if addr[0] != '/':
            addr = '/' + addr
        args = self.entry_args.get()
        arg_value = None
        if args != '':
            print(args)
            if args.startswith('"') and args.endswith('"'):
                arg_value = args
            elif len(list(filter(lambda a: args.startswith(a[0]) and args.endswith(a[1]), [('(', ')'), ('[', ']'), ('{', '}')]))) != 0:
                arg_value = eval(args)
            else:
                _splited = args.split()
                arg_value = map(lambda a: eval(a), _splited)
        self.client.command(addr, arg_value)

    def set_servo_pulsewidth(self, key, pulsewidth):
        self.machine.set_servo_pulsewidth(key, pulsewidth)

    def handlePIGPIO(self, event):
        logger.debug('event: %s', event.data)

    def handleQuit(self):
        self.server.close()
        self.root.destroy()


def start_gui(ip, port):
    stub = Stub(ip, port)
    driver = MachineDriver(stub)
    server = OSCServer(driver, ip=ip, port=port)

    stub.setup(server)
    stub.start()


if __name__ == '__main__':
    import argparse

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
    argsParser.add_argument('--debug', type=bool, default=True)

    args = argsParser.parse_args()
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    start_gui(args.ip, args.port)
