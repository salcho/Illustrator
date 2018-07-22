from math import sqrt, pow, ceil
from illustrator.Illustrator import Illustrator, CANVAS_DIMENSIONS


class CartesianIllustrator(Illustrator):
    def __init__(self, hat=None, canvasDimensions=None, initialPositions=None, beltLengths=None):
        super(CartesianIllustrator, self).__init__(hat, canvasDimensions, initialPositions, beltLengths)

    def getBeltLengthsFor(self, initialPositions):
        return self.triangleLengths(initialPositions)

    def go(self, x, y):
        print '--------- Going to: (%d, %d)' % (x, y)
        (targetLeft, targetRight) = self.triangleLengths((x, y))
        print 'targetLeft = %f, targetRight = %f' % (targetLeft, targetRight)

        (curLeft, curRight) = self.triangleLengths(self.currentPosition())
        print 'currentLeft = %f, currentRight: %f' % (curLeft, curRight)

        deltaLeft = int(-(curLeft - targetLeft))
        print 'deltaLeft = %f' % deltaLeft
        deltaRight = int(-(curRight - targetRight))
        print 'deltaRight = %f' % deltaRight

        denominator = max(deltaLeft, deltaRight)
        numerator = min(deltaLeft, deltaRight)
        rateOfChange = numerator / denominator

        while int(numerator):
            self.leftEngineQueue.put(ceil((1 if deltaLeft > 0 else -1 * (1 + rateOfChange)) * 10))
            self.rightEngineQueue.put((1 if deltaRight > 0 else -1) * 10)
            numerator = numerator - 1 if numerator > 0 else numerator + 1
            self.leftEngineQueue.join()
            self.rightEngineQueue.join()

        self._currentPosition = (x, y)
        '''
        if m == None:
            pass
        elif m == 0:
            pass
        else:
            i = 0
            j = 0
            xsign = -1 if deltaLeft < 0 else 1
            ysign = -1 if deltaRight < 0 else 1
            for cnt in range(max(abs(int(deltaLeft)), abs(int(deltaRight)))):
                if i < abs(deltaLeft):
                    self.leftEngine.move(xsign)
                    i += 1
                if j < abs(deltaRight):
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