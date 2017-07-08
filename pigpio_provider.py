'''pigpio mock'''
# -*- coding: utf-8 -*-
import logging
import os
import pigpio_gui

logger = logging.getLogger(__name__)
OUTPUT = 1

class Mock(object):
    '''Mock output callee property to stderr'''

    def __init__(self, name=''):
        self.name = name

    def __getattr__(self, attr):
        def wildcard(*args, **kwargs):
            logger.debug('%s: %s %s %s' % (self.name, attr, args, kwargs))

        if attr[:2] == '__' or (attr in dir(self)):
            raise AttributeError('Attribute %r not found' % (attr, ))
        else:
            return wildcard


class DummyPigpio:
    OUTPUT = 1
    _pi = Mock('pigpio')

    @classmethod
    def pi(cls):
        return cls._pi

def pi(mode=None, guiscreen=None):
    if mode != None and mode.upper() == 'GUI':
        _pigpio = pigpio_gui.PigpioGUIProvider(guiscreen)
    else:
        if os.uname().machine.startswith('arm'):
            import pigpio
            _pigpio = pigpio
        else:
            _pigpio = DummyPigpio
    OUTPUT = _pigpio.OUTPUT

    return _pigpio.pi()


