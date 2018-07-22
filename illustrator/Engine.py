import abc
from test.TestClasses import TestHat


class Engine(object):
    __metaclass__ = abc.ABCMeta
    STEPPER_SPEED = 10
    stepsPerPhase = 200
    STEPS_PER_MM = 10
    forward = TestHat.FORWARD
    backward = TestHat.BACKWARD
    style = TestHat.SINGLE
    DEBUG = 1

    def __init__(self, name, id, hat, initialPosition, beltLength):
        if initialPosition < 0 or initialPosition > beltLength:
            raise Exception("Invalid initial position for engine %d" % id)
        self.motorHat = hat
        self.name = name
        self.id = id
        self.engine = hat.getStepper(Engine.stepsPerPhase, id)
        self.engine.setSpeed(Engine.STEPPER_SPEED)
        self._curPosition = initialPosition
        self._beltLength = beltLength

    def __str__(self):
        return self.name

    def move(self, delta):
        if Engine.DEBUG: print '[%s]\tMoving %d from %d' % (self, delta, self._curPosition)
        if delta > 0:
            self.expand(delta)
        elif delta < 0:
            self.retract(delta)
        else:
            pass
        print '[%s] Current position: %d' % (self, self._curPosition)

    @abc.abstractmethod
    def retract(self, delta):
        raise NotImplemented("retract")

    @abc.abstractmethod
    def expand(self, delta):
        raise NotImplemented("expand")

    def currentPosition(self):
        return self._curPosition

    def beltLength(self):
        return self._beltLength

    def towardsUpperBoundary(self, direction, delta):
        if self._curPosition + delta >= self.beltLength():
            self.engine.step((self.beltLength() - self._curPosition)*Engine.STEPS_PER_MM, direction, Engine.style)
            self._curPosition = self.beltLength()
        else:
            self._curPosition += delta
            self.engine.step(int(delta)*Engine.STEPS_PER_MM, direction, Engine.style)

    def towardsLowerBoundary(self, direction, delta):
        if self._curPosition - delta <= 0:
            self.engine.step(self._curPosition*Engine.STEPS_PER_MM, direction, Engine.style)
            self._curPosition = 0
        else:
            self._curPosition -= delta
            self.engine.step(int(delta)*Engine.STEPS_PER_MM, direction, Engine.style)

class LeftEngine(Engine):
    def retract(self, delta):
        self.towardsLowerBoundary(Engine.backward, abs(delta))
        return self

    def expand(self, delta):
        self.towardsUpperBoundary(Engine.forward, abs(delta))
        return self

class RightEngine(Engine):
    def retract(self, delta):
        self.towardsLowerBoundary(Engine.forward, abs(delta))
        return self

    def expand(self, delta):
        self.towardsUpperBoundary(Engine.backward, abs(delta))
        return self
