from math import sqrt, pow

from illustrator.Illustrator import Illustrator, MOTOR_DISTANCE


class CartesianIllustrator(Illustrator):
    def __init__(self, hat=None, canvasDimensions=None, initialPositions=None, beltLengths=None):
        super(CartesianIllustrator, self).__init__(hat, canvasDimensions, initialPositions, beltLengths)

    def go(self, x, y):
        m, b = self.findStraightLineTo(x, y)  # TODO: Do we really need this?
        print 'current position: (%d, %d)' % (self._currentPosition[0], self._currentPosition[1])
        print 'going to : (%d, %d)' % (x, y)
        if not m:
            print 'm is none'
        else:
            print 'm = %f, b = %f' % (m, b)
        (targetLeft, targetRight) = self.triangleLengths((x, y))
        print 'targetLeft = %f, targetRight = %f' % (targetLeft, targetRight)

        (curLeft, curRight) = self.triangleLengths(self.currentPosition())
        print 'current triangle: (%d, %d)' % (curLeft, curRight)
        deltaX = -(curLeft - targetLeft)
        print 'deltaX = %f' % deltaX
        deltaY = -(curRight - targetRight)
        print 'deltaY = %f' % deltaY

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

    def areClose(self, a, b, rel_tol=1e-09, abs_tol=0.0):
        return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

    def triangleLengths(self, coords):
        x = coords[0]
        y = coords[1]
        if x < 0 or y < 0:
            raise Exception("Negative coords: (%d, %d)" % (x, y))
        if x > MOTOR_DISTANCE and not self.areClose(x, MOTOR_DISTANCE):
            raise Exception("x coordinate out of bounds: (%d > %d)" % (x, MOTOR_DISTANCE))

        return (sqrt(pow(x, 2) + pow(y, 2)),
                sqrt(pow(MOTOR_DISTANCE - x, 2) + pow(y, 2)))


def cartesianCoords(lengths):
    leftLength = lengths[0]
    rightLength = lengths[1]
    if leftLength * rightLength < 1 or leftLength + rightLength < 0:
        raise Exception("Negative or zero triangle lengths: (%d, %d)" % (leftLength, rightLength))

    semi = (MOTOR_DISTANCE + leftLength + rightLength) / 2
    if MOTOR_DISTANCE >= semi:
        raise Exception("Lengths are too short: impossible triangle")

    y = (2.0 / MOTOR_DISTANCE) * (
        sqrt(semi * (semi - leftLength) * (semi - rightLength) * (semi - MOTOR_DISTANCE)))
    x = sqrt(pow(float(leftLength), 2) - pow(float(y), 2))
    return (x, y)