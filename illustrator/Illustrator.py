from Queue import LifoQueue, Queue

from illustrator.Engine import Engine, LeftEngine, RightEngine
from math import sqrt, pow
import atexit


class Illustrator(object):
    MOTOR_DISTANCE = 40

    STEP_IN_MM = 1  # Resolution at which to calculate path

    # initialPositions -> (x, y) initial gondola position
    def __init__(self, hat, canvasDimensions, initialPositions, beltLengths):
        if not hat:
            raise Exception("Null HAT. No engines :(")
        self.motorHat = hat

        width, height = canvasDimensions
        if width * height < 1 or width + height < 0:
            raise Exception("Negative or zero canvas dimensions (%d, %d)" % (width, height))
        self.canvasWidth = width
        self.canvasHeight = height

        if Engine.DEBUG:
            self.isValidInitialPos(beltLengths, initialPositions)
            self.areBeltsBigEnough(beltLengths, height)

        self.createEngines(beltLengths, initialPositions)
        self._currentPosition = initialPositions  # in (x, y) coords

    def isValidInitialPos(self, beltLengths, initialPositions):
        if (initialPositions[0] > beltLengths[0] or initialPositions[1] > beltLengths[1]):
            raise Exception("Initial position (%f, %f) is out-bounds: (%f, %f)" % (initialPositions[0],
                                                                                   initialPositions[0],
                                                                                   beltLengths[0],
                                                                                   beltLengths[0]))

    def createEngines(self, beltLengths, initialPositions):
        self.leftEngine = LeftEngine("leftStepper", 1, self.motorHat, initialPositions[0], beltLengths[0])
        self.rightEngine = RightEngine("rightStepper", 2, self.motorHat, initialPositions[1], beltLengths[1])

    def areBeltsBigEnough(self, beltLengths, height):
        hypothenuse = sqrt(pow(Illustrator.MOTOR_DISTANCE, 2) + pow(height, 2))
        if (beltLengths[0] <= hypothenuse and not areClose(beltLengths[0], hypothenuse)) \
                or (beltLengths[1] <= hypothenuse and not areClose(beltLengths[1], hypothenuse)):
            raise Exception("Belts aren't big enough: (%f, %f) ; minimum length is: %f" % (beltLengths[0],
                                                                                           beltLengths[1],

                                                                                           hypothenuse))

    def _turnOff(self):
        self.motorHat.getMotor(1).run(self.motorHat.RELEASE)
        self.motorHat.getMotor(3).run(self.motorHat.RELEASE)
        self.motorHat.getMotor(2).run(self.motorHat.RELEASE)
        self.motorHat.getMotor(4).run(self.motorHat.RELEASE)

    def start(self, findHome=False):
        atexit.register(self._turnOff)
        if findHome:
            self.go(0, 0)

        return self

    def go(self, x, y):
        m, b = self.findStraightLineTo(x, y)  # TODO: Do we really need this?
        print 'current position: (%d, %d)' % (self._currentPosition[0], self._currentPosition[1])
        print 'going to : (%d, %d)' % (x,y)
        if m == None: print 'm is none'
        else:
            print 'm = %f, b = %f' % (m, b)
        (targetLeft, targetRight) = triangleLengths((x, y))
        print 'targetLeft = %f, targetRight = %f' % (targetLeft, targetRight)

        (curLeft, curRight) = triangleLengths(self.currentPosition())
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
    def currentPosition(self):
        return self._currentPosition

    def findStraightLineTo(self, x, y):
        x = float(x)
        y = float(y)

        m = None
        try:
            m = (self._currentPosition[1] - y) / (self._currentPosition[0] - x)
        except ZeroDivisionError:
            return (m, None)  # Slope is infinite - vertical movement

        b = y - m * x
        return (m, b)


def triangleLengths(coords):
    x = coords[0]
    y = coords[1]
    if x < 0 or y < 0:
        raise Exception("Negative coords: (%d, %d)" % (x, y))
    if x > Illustrator.MOTOR_DISTANCE and not areClose(x, Illustrator.MOTOR_DISTANCE):
        raise Exception("x coordinate out of bounds: (%d > %d)" % (x, Illustrator.MOTOR_DISTANCE))

    return (sqrt(pow(x, 2) + pow(y, 2)),
            sqrt(pow(Illustrator.MOTOR_DISTANCE - x, 2) + pow(y, 2)))


def cartesianCoords(lengths):
    leftLength = lengths[0]
    rightLength = lengths[1]
    if leftLength * rightLength < 1 or leftLength + rightLength < 0:
        raise Exception("Negative or zero triangle lengths: (%d, %d)" % (leftLength, rightLength))

    semi = (Illustrator.MOTOR_DISTANCE + leftLength + rightLength) / 2
    if Illustrator.MOTOR_DISTANCE >= semi:
        raise Exception("Lengths are too short: impossible triangle")

    y = (2.0 / Illustrator.MOTOR_DISTANCE) * (
    sqrt(semi * (semi - leftLength) * (semi - rightLength) * (semi - Illustrator.MOTOR_DISTANCE)))
    x = sqrt(pow(float(leftLength), 2) - pow(float(y), 2))
    return (x, y)


def areClose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)
