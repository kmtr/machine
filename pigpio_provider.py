'''pigpio mock'''
# -*- coding: utf-8 -*-
import logging
import os

logger = logging.getLogger(__name__)


class Mock(object):
    '''Mock output callee property to stderr'''

    def __init__(self, name=''):
        self.name = name

    def __getattr__(self, attr):
        def wildcard(*args, **kwargs):
            logger.debug('{}: {} {} {}'.format(
                self.name, attr, args, kwargs))
        if attr[:2] == '__' or (attr in dir(self)):
            raise AttributeError('Attribute %r not found' % (attr,))
        else:
            return wildcard


class DummyPigpio:
    OUTPUT = 'pigpio.OUTPUT'
    _pi = Mock('pigpio')

    @classmethod
    def pi(cls):
        return cls._pi


if os.uname().machine.startswith('arm'):
    import pigpio
    _pigpio = pigpio
else:
    _pigpio = DummyPigpio


def pi():
    return _pigpio.pi()


OUTPUT = _pigpio.OUTPUT
