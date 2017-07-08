'''Machine Controler'''
# -*- coding: utf-8 -*-
import logging
import time
import threading

import pigpio_provider

logger = logging.getLogger(__name__)


class Pin:
    '''
    It is pigpio wrapper
    '''

    def __init__(self, gpio, wait=0.5):
        '''
        initialize pin
        @param gpio GPIO number
        @param wait to save GPIO
        '''
        self.wait = wait
        self.pin = gpio
        self.sem = threading.Semaphore()

    def setup(self, pigpiopi):
        '''
        @param pigpiopi connection to pi. It is generated pigpio.pi()
        '''
        pigpiopi.set_mode(self.pin, pigpio_provider.OUTPUT)

    def set_servo_pulsewidth(self, pigpiopi, pulsewidth: int):
        '''
        call pigpio.set_servo_pulsewidth.
        if pulsewidth < 500 then set 500 and 2500 < pulsewidth set 2500.
        It is for safety.

        @param pigpiopi connection to pi. It is generated pigpio.pi()
        @param pulsewidth about(500 <= 1500 <= 2500)
        '''
        pin_thread = threading.Thread(
            target=self._set_servo_pulsewidth, args=(pigpiopi, pulsewidth))
        pin_thread.start()

    def _set_servo_pulsewidth(self, pigpiopi, pulsewidth: int):
        if pulsewidth < 500:
            pulsewidth = 500
        if pulsewidth > 2500:
            pulsewidth = 2500
        with self.sem:
            logger.debug(
                'GPIO={}, pulsewidth={} start'.format(self.pin, pulsewidth))
            pigpiopi.set_servo_pulsewidth(self.pin, pulsewidth)
            time.sleep(self.wait)
            logger.debug(
                'GPIO={}, pulsewidth={} done'.format(self.pin, pulsewidth))


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
        # 8: 10,
        # 9: 11,
        # 10: 12,
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

    def set_servo_pulsewidth(self, key: int, pulsewidth: int):
        '''
        @param pigpiopi connection to pi. It is generated pigpio.pi()
        @param pulsewidth 500 <= 1500 <= 2500
        '''
        pin = self.pins[key]
        pin.set_servo_pulsewidth(self.pigpiopi, pulsewidth)

    def set_servo_degree(self, key: int, degree: int):
        '''
        @param pigpiopi connection to pi. It is generated pigpio.pi()
        @param degree 0 <= degree <= 180
        '''
        if degree < 0:
            degree = 0
        if degree > 180:
            degree = 180

        pulsewidth = degree * 11.11111 + 500
        self.set_servo_pulsewidth(key, round(pulsewidth))

    def set_servo_degree_pattern(self, pattern):
        logger.info(pattern.name)
        for i, degree in enumerate(pattern.degrees):
            self.set_servo_degree(i, degree)


if __name__ == '__main__':
    from patterns import PATTERNS
    logging.basicConfig(level=logging.DEBUG)

    pi = pigpio_provider.pi()
    machine = Machine(pi)
    machine.setup()

    for i in range(2):
        machine.set_servo_degree(0, 90)
        machine.set_servo_degree(1, 0)
        machine.set_servo_degree_pattern(PATTERNS[i])

    time.sleep(6)
