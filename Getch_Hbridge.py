#!/usr/bin/env python 
import RPi.GPIO as gpio
import time, sys

class _Getch:
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()

class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()

def Setup():
    gpio.setmode(gpio.BOARD)

    #right
    gpio.setup(7, gpio.OUT)
    gpio.setup(11, gpio.OUT)
    gpio.setup(13, gpio.OUT)
    gpio.setup(15, gpio.OUT)
    #right init are just "on"
    gpio.output(7, True)
    gpio.output(11, True)

    #left
    gpio.setup(12, gpio.OUT)
    gpio.setup(16, gpio.OUT)
    gpio.setup(18, gpio.OUT)
    gpio.setup(22, gpio.OUT)
    #left init are just "on"
    gpio.output(12, True)
    gpio.output(16, True)

def QuitIt():
	sys.exit()

def getInput():
	got = int(raw_input('--> '))
	return got

# Right Forward gpio.output(15, True)
# Right Reverse gpio.output(13, True)

# Left  Forward gpio.output(18, True)
# Left  Reverse gpio.output(22, True)


def action(key):
    global delay
    if key == 'w':
        print "Forward"
        gpio.output(15, True)
        gpio.output(18, True)
        time.sleep(delay)
        gpio.output(15, False)
        gpio.output(18, False)

    if key == 's':
        print "Reverse"
        gpio.output(13, True)
        gpio.output(22, True)
        time.sleep(delay)
        gpio.output(13, False)
        gpio.output(22, False)

    if key == 'a':
        print "Left Pivot"
        gpio.output(15, True)
        gpio.output(22, True)
        time.sleep(delay)
        gpio.output(15, False)
        gpio.output(22, False)

    if key == 'd':
        print "Right Pivot"
        gpio.output(18, True)
        gpio.output(13, True)
        time.sleep(delay)
        gpio.output(18, False)
        gpio.output(13, False)

    if key == 'l':
        delay = delay + 0.1
        print ("Delay Up: " + str(delay))

    if key == 'k':
        delay = delay - 0.1
        print ("Delay Dw: " + str(delay))

    if key == 'q':
        print "Quit"
        QuitIt()

delay = 0.2

getch = _Getch()

Setup()

while True:
	action(getch())