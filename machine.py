'''Machine Controler'''
# -*- coding: utf-8 -*-
import logging
import time

try:
    import pigpio
except ImportError:
    import mock as pigpio

logger = logging.getLogger(__name__)


class Pin:
    '''
    It is pigpio wrapper
    '''

    def __init__(self, gpio):
        '''
        initialize pin
        @param gpio GPIO number
        '''
        self.pin = gpio

    def setup(self, pigpiopi):
        '''
        @param pigpiopi connection to pi. It is generated pigpio.pi()
        '''
        pigpiopi.set_mode(self.pin, pigpio.OUTPUT)

    def set_servo_pulsewidth(self, pigpiopi, pulsewidth):
        '''
        call pigpio.set_servo_pulsewidth.
        if pulsewidth < 500 then set 500 and 2500 < pulsewidth set 2500.
        It is for safety.

        @param pigpiopi connection to pi. It is generated pigpio.pi()
        @param pulsewidth about(500 <= 1500 <= 2500)
        '''
        if pulsewidth < 500:
            pulsewidth = 500
        if pulsewidth > 2500:
            pulsewidth = 2500
        logger.debug('GPIO={}, pulsewidth={}'.format(self.pin, pulsewidth))
        return pigpiopi.set_servo_pulsewidth(self.pin, pulsewidth)


class Machine:
    '''
    Machine
    '''
    KEY_GPIO_MAP = {
        # KEY : GPIO
        0: 2,
        1: 3,
        2: 4,
        3: 5,
        4: 6,
        5: 7,
        6: 8,
        7: 9,
        8: 10,
        9: 11,
        10: 12,
    }
    '''
    KEY_GPIO_MAP represents mappings logical key ans GPIO
    http://abyz.co.uk/rpi/pigpio/#Type_3
    '''

    def __init__(self, pigpiopi):
        '''
        @param pigpiopi
        '''
        self.pigpiopi = pigpiopi
        self.pins = {}
        for k, gpio in Machine.KEY_GPIO_MAP.items():
            self.pins[k] = Pin(gpio)

    def setup(self):
        for pin in self.pins.values():
            pin.setup(self.pigpiopi)

    def close(self):
        self.pigpiopi.stop()

    def set_servo_pulsewidth(self, key, pulsewidth):
        return self.pins[key].set_servo_pulsewidth(self.pigpiopi, pulsewidth)

    def set_servo_degree(self, key, degree):
        '''
        @param pigpiopi connection to pi. It is generated pigpio.pi()
        @param degree 0 <= dgredd <= 180
        '''
        if degree < 0:
            degree = 0
        if degree > 180:
            degree = 180

        pulsewidth = degree * 11.11111 + 500
        return self.set_servo_pulsewidth(key, round(pulsewidth))

    def set_servo_degree_pattern(self, pattern):
        logger.info(pattern.name)
        for i, degree in enumerate(pattern.degrees):
            self.set_servo_degree(i, degree)


if __name__ == '__main__':
    from patterns import PATTERNS
    logging.basicConfig(level=logging.DEBUG)

    pi = pigpio.pi()
    machine = Machine(pi)
    machine.setup()
    machine.set_servo_degree(0, 90)
    machine.set_servo_degree_pattern(PATTERNS[-1])
