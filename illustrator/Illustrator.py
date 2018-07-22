from Queue import Queue
import abc
import atexit
from math import sqrt, pow

from illustrator.Engine import Engine, LeftEngine, RightEngine

CANVAS_DIMENSIONS = 40

class Draws(object):
    @abc.abstractmethod
    def draw(self, id):
        raise NotImplemented("draw")


class Illustrator(Draws):
    STEP_IN_MM = 1  # Resolution at which to calculate path

    # initialPositions -> (x, y) initial gondola position
    def __init__(self, hat = None, canvasDimensions = None, initialPositions = None, beltLengths = None):
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

        initialBeltLengths = self.getBeltLengthsFor(initialPositions)
        print "Initial belt lengths are: (%d, %d)" % (initialBeltLengths[0], initialBeltLengths[1])
        self.createEngines(beltLengths, initialBeltLengths)

        self._currentPosition = initialPositions  # in (x, y) coords
        print "Initial position is: (%d, %d)" % (self._currentPosition[0], self._currentPosition[1])

    def go(self, x, y):
        raise NotImplemented("go")

    @abc.abstractmethod
    def areClose(self, a, b, rel_tol=1e-09, abs_tol=0.0):
        pass

    @abc.abstractmethod
    def areBeltsBigEnough(self, beltLengths, height):
        hypothenuse = sqrt(pow(CANVAS_DIMENSIONS, 2) + pow(height, 2))
        # TODO: belts should be smaller. full stop.
        if (beltLengths[0] <= hypothenuse and not self.areClose(beltLengths[0], hypothenuse)) \
                or (beltLengths[1] <= hypothenuse and not self.areClose(beltLengths[1], hypothenuse)):
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

    def isValidInitialPos(self, beltLengths, initialPositions):
        if initialPositions[0] > beltLengths[0] or initialPositions[1] > beltLengths[1]:
            raise Exception("Initial position (%f, %f) is out-bounds: (%f, %f)" % (initialPositions[0],
                                                                                   initialPositions[0],
                                                                                   beltLengths[0],
                                                                                   beltLengths[0]))

    def createEngines(self, beltLengths, initialPositions):
        self.leftEngineQueue = Queue()
        self.rightEngineQueue = Queue()

        # CONVENTION: Start with the left belt completely retracted
        self.leftEngine = LeftEngine("leftStepper", 1, self.motorHat, initialPositions[0], beltLengths[0])
        self.rightEngine = RightEngine("rightStepper", 2, self.motorHat, initialPositions[1], beltLengths[1],)

    @abc.abstractmethod
    def getBeltLengthsFor(self, initialPositions):
        pass
