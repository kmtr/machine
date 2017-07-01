# -*- coding: utf-8 -*-
class Pattern:
    def __init__(self, name, degrees=[0, 0, 0, 0, 0, 0, 0, 0]):
        self.name = name
        self.degrees = degrees


PATTERN_RESET = Pattern('reset')

PATTERNS = {
    -1: PATTERN_RESET,
    0: Pattern('I', [
        0, 0, 0, 0,  # LEFT
        0, 0, 0, 0,  # RIGHT
    ]),
    1: Pattern('L', [
        180, 0, 0, 0,  # LEFT
        90, 0, 0, 0,  # RIGHT
    ]),
    2: Pattern('r-L', [
        90, 0, 0, 0,  # LEFT
        180, 0, 0, 0,  # RIGHT
    ]),
    3: Pattern('slash-r', [
        60, 0, 0, 0,   # LEFT
        120, 0, 0, 0,  # RIGHT
    ]),
    4: Pattern('slash-l', [
        120, 0, 0, 0,  # LEFT
        60, 0, 0, 0,  # RIGHT
    ]),
    5: Pattern('Koshi ni Te', [
        80, 0, 0, 115,  # LEFT
        80, 0, 0, 115,  # RIGHT
    ]),
    6: Pattern('Y', [
        160, 0, 0, 0,  # LEFT
        160, 0, 0, 0,  # RIGHT
    ]),
    7: Pattern('T', [
        90, 0, 0, 0,  # LEFT
        90, 0, 0, 0,  # RIGHT
    ]),
    8: Pattern('Y', [
        170, 0, 0, 0,  # LEFT
        170, 0, 0, 0,  # RIGHT
    ]),
    9: Pattern('katate-up-R', [
        0, 0, 0, 0,  # LEFT
        150, 0, 0, 0,  # RIGHT
    ]),
    10: Pattern('katate-down-R', [
        0, 0, 0, 0,  # LEFT
        60, 0, 0, 0,  # RIGHT
    ]),
    11: Pattern('katate-up-L', [
        150, 0, 0, 0,  # LEFT
        0, 0, 0, 0,  # RIGHT
    ]),
    12: Pattern('katate-down-L', [
        60, 0, 0, 0,  # LEFT
        0, 0, 0, 0,  # RIGHT
    ]),
    13: Pattern('Naname-down', [
        60, 0, 0, 0,  # LEFT
        60, 0, 0, 0,  # RIGHT
    ]),
}
