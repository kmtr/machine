# -*- coding: utf-8 -*-
import logging
import tkinter
import turtle
from typing import Dict

logger = logging.getLogger(__name__)


class Arm:
    def __init__(self, length: int, child_arm=None):
        self.length = length
        self.child_arm = child_arm

    def draw(self, kame: turtle.RawTurtle, degree, mag=1, color='black'):
        kame.setheading(270)
        kame.lt(degree)
        kame.color(color)
        kame.fd(self.length * mag)
        if self.child_arm:
            kame.setheading(270)
            kame.fd(self.child_arm.length * mag)


class Leg:

    FACE_FRONT = 1
    FACE_BACK = -1

    def __init__(self, height, arm_pos, arm: Arm, face, pos=(0, 0), base=0):
        self.height = height
        self.arm_pos = arm_pos
        self.arm = arm
        self.pulsewidth = 500
        if face < 0:
            self.face = -1
        else:
            self.face = 1
        self.pos = pos

    def setup(self, screen, arm_color='black'):
        self.screen = screen
        self.kame = turtle.RawTurtle(self.screen, visible=False)
        self.arm_color = arm_color
        self.draw_leg()
        self.degree = 0

    def draw_leg(self):
        mag = PigpioGUI.mag
        self.kame.reset()
        self.kame.ht()
        self.kame.speed(0)
        self.kame.up()
        self.kame.setpos(self.pos[0], self.pos[1] - 100)
        self.kame.down()
        self.kame.lt(90)
        self.kame.fd(self.height * mag)
        self.kame.bk((self.height - self.arm_pos) * mag)
        self.screen.update()

    def draw_arm(self, degree, mag):
        self.arm.draw(self.kame, degree * self.face, mag, self.arm_color)

    def set_servo_pulsewidth(self, pulsewidth):
        if self.pulsewidth == pulsewidth:
            return
        self.pulsewidth = pulsewidth
        mag = PigpioGUI.mag
        degree = round(pulsewidth - 500) / 11.11111
        self.draw_leg()
        self.draw_arm(degree, mag)
        self.screen.update()


class PigpioGUI:

    mag = 10
    _colors = [
        'red', 'orange', 'spring green', 'blue', 'purple', 'RosyBrown',
        'sea green', 'turquoise', 'maroon', 'firebrick', 'cyan', 'coral',
        'DarkGoldenrod', 'plum4', 'tan4'
    ]

    def __init__(self, screen: turtle.TurtleScreen, legs: Dict[int, Leg]):
        self.legs = legs
        for gpio, leg in legs.items():
            leg.setup(screen, self._colors[gpio])

    def set_mode(self, gpio: int, mode: int):
        logger.debug('set_mode: %s %s' % (gpio, mode))

    def set_servo_pulsewidth(self, gpio: int, pulsewidth: int):
        leg = self.legs[gpio]
        leg.set_servo_pulsewidth(pulsewidth)

    def stop(self):
        pass


class PigpioGUIProvider:

    screen = None

    OUTPUT = 1

    def __init__(self, screen):
        self.screen = screen

    def buildLegs(self):
        pos = (0, 0)
        return {
            2: Leg(10, 8, Arm(5), Leg.FACE_FRONT, pos),
            3: Leg(10, 8, Arm(5), Leg.FACE_BACK, pos),
            4: Leg(10, 8, Arm(5), Leg.FACE_FRONT, pos),
            5: Leg(10, 8, Arm(5), Leg.FACE_BACK, pos),
            6: Leg(10, 8, Arm(5, Arm(3)), Leg.FACE_FRONT, pos),
            7: Leg(10, 8, Arm(5, Arm(3)), Leg.FACE_BACK, pos),
            8: Leg(10, 8, Arm(5), Leg.FACE_FRONT, pos),
            9: Leg(10, 8, Arm(5), Leg.FACE_BACK, pos),
            10: Leg(10, 8, Arm(5), Leg.FACE_FRONT, pos),
            11: Leg(10, 8, Arm(5), Leg.FACE_BACK, pos),
        }

    def pi(self):
        return PigpioGUI(self.screen, self.buildLegs())


if __name__ == '__main__':
    import pigpio_provider

    root = tkinter.Tk()
    canvas = tkinter.Canvas(root)
    screen = turtle.TurtleScreen(canvas)
    screen.tracer(0, 0)

    stub = pigpio_provider.pi('GUI', screen)

    canvas.pack()

    root.after(200, stub.set_servo_pulsewidth, 2, 750)
    root.after(400, stub.set_servo_pulsewidth, 3, 1500)
    root.after(600, stub.set_servo_pulsewidth, 4, 500)
    root.after(800, stub.set_servo_pulsewidth, 2, 900)
    root.after(1000, stub.set_servo_pulsewidth, 6, 900)
    root.after(1200, stub.set_servo_pulsewidth, 7, 900)

    root.mainloop()