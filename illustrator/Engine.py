import abc
from threading import Thread

FORWARD = -1
BACKWARD = -1
STYLE = -1

try:
    from Adafruit_MotorHAT import Adafruit_MotorHAT
    FORWARD = Adafruit_MotorHAT.FORWARD
    BACKWARD = Adafruit_MotorHAT.BACKWARD
    STYLE = Adafruit_MotorHAT.SINGLE
except:
    FORWARD = 1
    BACKWARD = 2
    STYLE = 3
    pass

from test.TestClasses import TestHat

class Engine(object):
    __metaclass__ = abc.ABCMeta
    STEPPER_SPEED = 10
    stepsPerPhase = 200
    STEPS_PER_MM = 10
    style = 1 # Adafruit_MotorHAT.SINGLE
    DEBUG = 1

    def __init__(self, name, id, hat, initialPosition, beltLength, instructionQueue):
        if initialPosition < 0 or initialPosition > beltLength:
            raise Exception("Invalid initial position for engine %d" % id)
        self.motorHat = hat
        self.name = name
        self.id = id
        self.engine = hat.getStepper(Engine.stepsPerPhase, id)
        self.engine.setSpeed(Engine.STEPPER_SPEED)
        self._curLength = initialPosition
        self._maxLength = beltLength
        self.q = instructionQueue
        self.thread = Thread(target=self.moveToLength)
        self.thread.daemon = True
        self.thread.start()

    def moveToLength(self):
        while True:
            length = self.q.get()
            print '[%s] Going to length %d from %d' % (self, length, self._curLength)
            delta = self._curLength - length
            self.move(delta)
            self.q.task_done()

    def __str__(self):
        return self.name

    def move(self, delta):
        if delta > 0:
            if Engine.DEBUG: print '[%s]\tExpanding %d from %d' % (self, delta, self._curLength)
            self.expand(delta)
        elif delta < 0:
            if Engine.DEBUG: print '[%s]\tRetracting %d from %d' % (self, delta, self._curLength)
            self.retract(delta)
        else:
            pass
        print '[%s] Current position: %d' % (self, self._curLength)

    @abc.abstractmethod
    def retract(self, delta):
        raise NotImplemented("retract")

    @abc.abstractmethod
    def expand(self, delta):
        raise NotImplemented("expand")

    def currentLength(self):
        return self._curLength

    def beltLength(self):
        return self._maxLength

    def towardsUpperBoundary(self, direction, delta):
        if self._curLength + delta >= self.beltLength():
            self.engine.step((self.beltLength() - int(self._curLength)) * Engine.STEPS_PER_MM, direction, Engine.style)
            self._curLength = self.beltLength()
        else:
            self._curLength += delta
            steps = int(delta) * Engine.STEPS_PER_MM
            if Engine.DEBUG:
                print '[%s] Steps per mm: %d towards %s' % (self, steps, direction)

            self.engine.step(steps, direction, Engine.style)

    def towardsLowerBoundary(self, direction, delta):
        if self._curLength - delta <= 0:
            self.engine.step(int(self._curLength) * Engine.STEPS_PER_MM, direction, Engine.style)
            self._curLength = 0
        else:
            self._curLength -= delta
            steps = int(delta) * Engine.STEPS_PER_MM
            if Engine.DEBUG:
                print '[%s] Steps per mm: %d towards %s' % (self, steps, direction)
            self.engine.step(steps, direction, Engine.style)

class LeftEngine(Engine):

    def retract(self, delta):
        self.towardsLowerBoundary(BACKWARD, abs(delta))
        return self

    def expand(self, delta):
        self.towardsUpperBoundary(FORWARD, abs(delta))
        return self

class RightEngine(Engine):
    def retract(self, delta):
        self.towardsLowerBoundary(FORWARD, abs(delta))
        return self

    def expand(self, delta):
        self.towardsUpperBoundary(BACKWARD, abs(delta))
        return self
