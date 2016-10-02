import abc
from threading import Thread
from test.TestClasses import TestHat


class Engine(object):
    __metaclass__ = abc.ABCMeta
    STEPPER_SPEED = 60
    stepsPerPhase = 200
    forward = TestHat.FORWARD
    backward = TestHat.BACKWARD
    style = TestHat.SINGLE

    def __init__(self, name, id, hat, initialPosition, beltLength, instructionQueue):
        if initialPosition < 0 or initialPosition > beltLength:
            raise Exception("Invalid initial position for engine %d" % id)
        self.motorHat = hat
        self.name = name
        self.id = id
        self.engine = hat.getStepper(Engine.stepsPerPhase, id)
        self.engine.setSpeed(Engine.STEPPER_SPEED)
        self._curPosition = initialPosition
        self._beltLength = beltLength
        self.q = instructionQueue
        self.thread = Thread(target=self.moveToLength)
        self.thread.daemon = True
        self.thread.start()

    def __str__(self):
        return self.name

    # TODO: Which is right, forward or backward? - this assumes left stepper
    def moveToLength(self):
        while True:
            length = self.q.get()
            print '[%s] Going to length %d from %d' % (self, length, self._curPosition)
            delta = int(self._curPosition) - int(length)
            if not delta:
                print 'delta is zero'
            elif delta > 0:
                self.retract(delta)
            else:
                self.expand(delta)
            print '[%s] Current position is: %d' % (self, self._curPosition)
            self.q.task_done()

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
            self._curPosition = self.beltLength()
            self.engine.step(self.beltLength() - self._curPosition, direction, Engine.style)
        else:
            self._curPosition += delta
            self.engine.step(int(delta), direction, Engine.style)

    def towardsLowerBoundary(self, direction, delta):
        if self._curPosition - delta < 0:
            self._curPosition = 0
            self.engine.step(self._curPosition, direction, Engine.style)
        else:
            self._curPosition -= delta
            self.engine.step(int(delta), direction, Engine.style)

class LeftEngine(Engine):
    def retract(self, delta):
        print 'left-retract'
        self.towardsLowerBoundary(Engine.backward, abs(delta))
        return self

    def expand(self, delta):
        print 'left-expand'
        self.towardsUpperBoundary(Engine.forward, abs(delta))
        return self

class RightEngine(Engine):
    def retract(self, delta):
        print 'right-retract'
        self.towardsLowerBoundary(Engine.forward, abs(delta))
        return self

    def expand(self, delta):
        print 'right-expand'
        self.towardsUpperBoundary(Engine.backward, abs(delta))
        return self