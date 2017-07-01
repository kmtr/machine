'''pigpio mock'''
# -*- coding: utf-8 -*-
import sys

OUTPUT = "pigpio.OUTPUT"

class Mock(object):
    '''Mock output callee property to stderr'''

    def __getattr__(self, attr):
        def wildcard(*args, **kwargs):
            print('MOCK: ' + attr, args, kwargs, file=sys.stderr)
        if attr[:2] == '__' or (attr in dir(self)):
            raise AttributeError('Attribute %r not found' % (attr,))
        else:
            return wildcard


def pi():
    '''create Mock instance
    pi() is a dummy of pigpio.pi()
    '''
    return Mock()
