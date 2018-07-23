from Adafruit_MotorHAT import *

from illustrator.CartesianIllustrator import CartesianIllustrator
from illustrator.Engine import Engine

hat = Adafruit_MotorHAT()
illustrator = CartesianIllustrator(hat, canvasDimensions=(30, 30), initialPositions=(0, 0), belt_lengths=(50, 50))
print '------------------'
print 'Canvas dimensions: (30, 30)'
print 'Initial positions: (0, 0)'
print 'Belt lengths: (50, 50)'
print '------------------'
illustrator.start()

orig = exit


def exit():
    print '\n[+] Motors off...'
    illustrator._turnOff()
    orig()


try:
    while True:
        x = -1
        y = -1
        try:
            x = raw_input('x ----> ')
            if x == 'exit':
                exit()
            elif x == 'setcm':
                val = raw_input('steps per cm ----> ')
                Engine.STEPS_PER_CM = int(val)
                continue
            elif x == 'setmm':
                val = raw_input('steps per cm ----> ')
                Engine.STEPS_PER_MM = int(val)
                continue

            x = int(x)
            y = int(raw_input('y ----> '))
        except ValueError:
            print "\n\n\n"
            continue

        if x == -1 or y == -1:
            continue

        illustrator.go(x, y)
        illustrator.join()
except KeyboardInterrupt:
    exit()
