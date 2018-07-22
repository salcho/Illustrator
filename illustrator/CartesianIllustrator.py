import logging
from math import sqrt, pow

from illustrator.Engine import Engine
from illustrator.Illustrator import Illustrator, CANVAS_DIMENSIONS


class CartesianIllustrator(Illustrator):
    def __init__(self, hat=None, canvasDimensions=None, initialPositions=None, beltLengths=None):
        if Engine.DEBUG:
            logging.basicConfig(
                level=logging.DEBUG,
                format="%(asctime)s %(levelname)-20s %(stepper)-20s %(message)s",
                datefmt='%H:%M:%S'
            )

        super(CartesianIllustrator, self).__init__(hat, canvasDimensions, initialPositions, beltLengths)

    def getBeltLengthsFor(self, initialPositions):
        return self.triangleLengths(initialPositions)

    def go(self, x, y):
        print '--------- Going to: (%d, %d)' % (x, y)
        (targetLeft, targetRight) = self.triangleLengths((x, y))
        print 'targetLeft = %f, targetRight = %f' % (targetLeft, targetRight)

        (curLeft, curRight) = self.triangleLengths(self.currentPosition())
        print 'currentLeft = %f, currentRight: %f' % (curLeft, curRight)

        deltaX = -(curLeft - targetLeft)
        print 'deltaX = %f' % deltaX
        deltaY = -(curRight - targetRight)
        print 'deltaY = %f' % deltaY

        self.leftEngineQueue.put(deltaX)
        self.rightEngineQueue.put(deltaY)
        self._currentPosition = (x, y)
        '''
        if m == None:
            pass
        elif m == 0:
            pass
        else:
            i = 0
            j = 0
            xsign = -1 if deltaX < 0 else 1
            ysign = -1 if deltaY < 0 else 1
            for cnt in range(max(abs(int(deltaX)), abs(int(deltaY)))):
                if i < abs(deltaX):
                    self.leftEngine.move(xsign)
                    i += 1
                if j < abs(deltaY):
                    for i in range(int(abs(m))):
                        self.rightEngine.move(ysign)
                        j += 1

        self._currentPosition = (x, y)
        pass
    '''

    def areClose(self, a, b, rel_tol=1e-09, abs_tol=0.0):
        return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

    def triangleLengths(self, coords):
        x = coords[0]
        y = coords[1]
        if x < 0 or y < 0:
            raise Exception("Negative coords: (%d, %d)" % (x, y))
        if x > CANVAS_DIMENSIONS and not self.areClose(x, CANVAS_DIMENSIONS):
            raise Exception("x coordinate out of bounds: (%d > %d)" % (x, CANVAS_DIMENSIONS))

        return (sqrt(pow(x, 2) + pow(y, 2)),
                sqrt(pow(CANVAS_DIMENSIONS - x, 2) + pow(y, 2)))


def cartesianCoords(lengths):
    leftLength = lengths[0]
    rightLength = lengths[1]
    if leftLength * rightLength < 1 or leftLength + rightLength < 0:
        raise Exception("Negative or zero triangle lengths: (%d, %d)" % (leftLength, rightLength))

    semi = (CANVAS_DIMENSIONS + leftLength + rightLength) / 2
    if CANVAS_DIMENSIONS >= semi:
        raise Exception("Lengths are too short: impossible triangle")

    y = (2.0 / CANVAS_DIMENSIONS) * (
        sqrt(semi * (semi - leftLength) * (semi - rightLength) * (semi - CANVAS_DIMENSIONS)))
    x = sqrt(pow(float(leftLength), 2) - pow(float(y), 2))
    return (x, y)