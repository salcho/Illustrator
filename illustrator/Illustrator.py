from Queue import LifoQueue, Queue

from illustrator.Engine import Engine
from math import sqrt, pow
import atexit

class Illustrator(object):
    MOTOR_DISTANCE = 40
    STEP_IN_MM = 1 # Resolution at which to calculate path

    # initialPositions -> (x, y) initial gondola position
    def __init__(self, hat, width, height, initialPositions, beltLengths):
        if not hat:
            raise Exception("Null hat instance passed to illustrator")
        self.motorHat = hat

        if width*height < 1:
            raise Exception("Negative or zero canvas dimensions (%d, %d)" % (width, height))
        self.canvasWidth = width
        self.canvasHeight = height

        left, right = triangleLengths(initialPositions)
        hypothenuse = sqrt(pow(Illustrator.MOTOR_DISTANCE, 2) + pow(height, 2))
        if (beltLengths[0] <= hypothenuse and not areClose(beltLengths[0], hypothenuse)) \
                or (beltLengths[1] <= hypothenuse and not areClose(beltLengths[1], hypothenuse)):
            raise Exception("Belts aren't big enough: (%f, %f) ; minimum length is: %f" % (beltLengths[0],
                                                                                           beltLengths[1],

                                                                                        hypothenuse))
        self.leftEngineQueue = Queue()
        self.rightEngineQueue = Queue()
        self.leftEngine = Engine("leftStepper", 1, self.motorHat, left, beltLengths[0], self.leftEngineQueue)
        self.rightEngine = Engine("rightStepper", 2, self.motorHat, right, beltLengths[1], self.rightEngineQueue)
        self._currentPosition = initialPositions # in (x, y) coords

    def _turnOff(self):
        self.motorHat.getMotor(1).run(self.motorHat.RELEASE)
        self.motorHat.getMotor(3).run(self.motorHat.RELEASE)
        self.motorHat.getMotor(2).run(self.motorHat.RELEASE)
        self.motorHat.getMotor(4).run(self.motorHat.RELEASE)

    def start(self, findHome = False):
        atexit.register(self._turnOff())
        if findHome:
            self.go(0, 0)

        return self

    def go(self, x, y):
        m, b = self.findStraightLineTo(x, y)   # TODO: Do we really need this?
        (targetLeft, targetRight) = triangleLengths((x,y))
        self.leftEngineQueue.put(targetLeft)
        self.rightEngineQueue.put(targetRight)
        self._currentPosition = (x, y)

    def currentPosition(self):
        return self._currentPosition

    def findStraightLineTo(self, x, y):
        x = float(x)
        y = float(y)
        m = None
        try:
            m = (self._currentPosition[1] - y)/(self._currentPosition[0] - x)
        except ZeroDivisionError:
            return (m, None) # Slope is infinite - vertical movement

        b = y - m*x
        return (m, b)



def triangleLengths(coords):
    leftSide = coords[0]
    rightSide = coords[1]
    if leftSide < 0 or rightSide < 0:
        raise Exception("Negative coords: (%d, %d)" % (leftSide, rightSide))
    if leftSide > Illustrator.MOTOR_DISTANCE and not areClose(leftSide, Illustrator.MOTOR_DISTANCE):
        raise Exception("x coordinate out of bounds: (%d > %d)" % (leftSide, Illustrator.MOTOR_DISTANCE))

    return (sqrt(pow(leftSide, 2) + pow(rightSide, 2)),
            sqrt(pow(Illustrator.MOTOR_DISTANCE - leftSide, 2) + pow(rightSide, 2)))

def cartesianCoords(lengths):
    leftLength = lengths[0]
    rightLength = lengths[1]
    if leftLength * rightLength < 1 or leftLength + rightLength < 0:
        raise Exception("Negative or zero triangle lengths: (%d, %d)" % (leftLength, rightLength))

    semi = (Illustrator.MOTOR_DISTANCE + leftLength + rightLength)/2
    if Illustrator.MOTOR_DISTANCE >= semi:
        raise Exception("Lengths are too short: impossible triangle")

    y = (2.0/Illustrator.MOTOR_DISTANCE)*(sqrt(semi * (semi - leftLength) * (semi - rightLength) * (semi - Illustrator.MOTOR_DISTANCE)))
    x = sqrt(pow(float(leftLength), 2) - pow(float(y), 2))
    return (x, y)

def areClose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)