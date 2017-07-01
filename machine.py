'''Machine Controler'''
# -*- coding: utf-8 -*-
try:
    import pigpio
except ImportError:
    import pigpio_mock as pigpio

class Pin:
    '''
    It is pigpio wrapper
    '''

    def __init__(self, gpio, mode=pigpio.OUTPUT):
        '''
        initialize pin
        @param gpio GPIO number
        @param mode pin mode (defualt pigpio.OUTPUT)
        '''
        self.pin = gpio
        self.mode = mode

    def setup(self, pigpiopi):
        '''
        @param pigpiopi connection to pi. It is generated pigpio.pi()
        '''
        pigpiopi.set_mode(self.pin, self.mode)

    def set_servo_pulsewidth(self, pigpiopi, pulsewidth):
        '''
        call pigpio.set_servo_pulsewidth.
        if pulsewidth < 500 then set 500 and 1500 < pulsewidth set 1500.
        It is for safety.

        @param pigpiopi connection to pi. It is generated pigpio.pi()
        @param pulsewidth about(500 <= 1500 <= 2500)
        @return return value of pigpiopi.set_servo_pulsewidth()
        '''
        if pulsewidth < 500:
            pulsewidth = 500
        if pulsewidth > 1500:
            pulsewidth = 1500
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


if __name__ == '__main__':
    pi = pigpio.pi()
    machine = Machine(pi)
    machine.setup()
    r = machine.set_servo_pulsewidth(0, 750)

    print(r)
