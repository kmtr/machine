'''pigpio mock'''
# -*- coding: utf-8 -*-
import logging
import sys

OUTPUT = "pigpio.OUTPUT"

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


def pi():
    '''create Mock instance
    pi() is a dummy of pigpio.pi()
    '''
    return Mock('pigpio')
