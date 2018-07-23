from math import sqrt, pow, ceil
from illustrator.Illustrator import Illustrator, CANVAS_DIMENSIONS


class CartesianIllustrator(Illustrator):
    def __init__(self, hat=None, canvasDimensions=None, initialPositions=None, belt_lengths=None):
        super(CartesianIllustrator, self).__init__(hat, canvasDimensions, initialPositions, belt_lengths)

    def getBeltLengthsFor(self, initial_positions):
        return self.triangleLengths(initial_positions)

    def go(self, x, y):
        print '--------- Going to: (%d, %d)' % (x, y)
        (target_left, target_right) = self.triangleLengths((x, y))
        print 'target_left = %f cm, target_right = %f cm' % (target_left, target_right)

        (curLeft, curRight) = self.triangleLengths(self.currentPosition())
        print 'currentLeft = %f cm, currentRight: %f cm' % (curLeft, curRight)

        deltaLeft = -(curLeft - target_left)
        print 'deltaLeft = %f cm' % deltaLeft
        deltaRight = -(curRight - target_right)
        print 'deltaRight = %f cm' % deltaRight

        denominator = max(deltaLeft, deltaRight)
        numerator = min(deltaLeft, deltaRight)
        rateOfChange = abs(numerator / denominator)
        print 'rate of change %f' % rateOfChange
        def increment(x):
            return x - 1 if deltaLeft > 0 else x + 1

        # each element in the queue represents a cm
        iterations = abs(int(numerator))
        print 'will run %d iterations' % iterations

        while iterations:
            if deltaLeft == numerator:
                self.queueLeft(deltaLeft, 0)
                self.queueRight(deltaRight, rateOfChange)
            else:
                self.queueLeft(deltaLeft, rateOfChange)
                self.queueRight(deltaRight, 0)

            self.rightEngineQueue.join()
            self.leftEngineQueue.join()

            iterations = increment(iterations)

        self._currentPosition = (x, y)


    def queueLeft(self, deltaLeft, rateOfChange):
        if deltaLeft > 0:
            self.leftEngineQueue.put(1 + rateOfChange)
        else:
            self.leftEngineQueue.put(-1 - rateOfChange)

    def queueRight(self, deltaRight, rateOfChange):
        if deltaRight > 0:
            self.rightEngineQueue.put(1 + rateOfChange)
        else:
            self.rightEngineQueue.put(-1 - rateOfChange)

    def areClose(self, a, b, rel_tol=1e-09, abs_tol=0.0):
        return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

    # noinspection PyPep8Naming
    def triangleLengths(self, coords):
        x = coords[0]
        y = coords[1]
        if x < 0 or y < 0:
            raise Exception("Negative coords: (%d, %d)" % (x, y))
        if x > CANVAS_DIMENSIONS and not self.areClose(x, CANVAS_DIMENSIONS):
            raise Exception("x coordinate out of bounds: (%d > %d)" % (x, CANVAS_DIMENSIONS))

        return (sqrt(pow(x, 2) + pow(y, 2)), sqrt(pow(CANVAS_DIMENSIONS - x, 2) + pow(y, 2)))


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