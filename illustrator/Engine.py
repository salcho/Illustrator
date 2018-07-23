import abc
import logging
from math import ceil, floor
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

class Engine(object):
    __metaclass__ = abc.ABCMeta
    STEPPER_SPEED = 10
    stepsPerPhase = 200
    STEPS_PER_CM = 10
    STEPS_PER_MM = 5
    DEBUG = 1

    def __init__(self, name, id, hat, initialPosition, beltLength, instructionQueue, logger=logging.getLogger('Engine')):
        self.logger = logger

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

    def log(self, msg):
        if Engine.DEBUG:
            #self.logger.debug(msg, extra={"stepper": str(self)})
            print '%-20s %s' % (self, msg)

    def moveToLength(self):
        while True:
            delta = self.q.get()
            initial_pos = self._curLength

            if delta > 0:
                self.expand_delta(delta)
            elif delta < 0:
                self.retract_delta(abs(delta))
            else:
                pass

            self.log('%0.2f -> to -> %0.2f  | final length: %0.2f' % (initial_pos, initial_pos + delta, self._curLength))

            self.q.task_done()

    def __str__(self):
        return self.name

    @abc.abstractmethod
    def retract_single(self, unit):
        raise NotImplemented("retract")

    @abc.abstractmethod
    def expand_single(self, unit):
        raise NotImplemented("expand")

    def currentLength(self):
        return self._curLength

    def beltLength(self):
        return self._maxLength

    def towardsUpperBoundary(self, direction, unit):
        delta = 1 # cm

        if self._curLength + delta >= self.beltLength():
            steps = (self.beltLength() - int(self._curLength)) * unit
            if Engine.DEBUG:
                self.log('[%s] Moving to boundary. [%d] %s\n' % (self, steps, fromInt(direction)))

            self.engine.step(steps, direction, STYLE)
            self._curLength = self.beltLength()
        else:
            self.engine.step(unit, direction, STYLE)

    def towardsLowerBoundary(self, direction, unit):
        delta = 1

        if self._curLength - delta <= 0:
            steps = int(self._curLength) * unit
            if Engine.DEBUG:
                self.log('[%s] Moving to boundary. [%d] %s\n' % (self, steps, fromInt(direction)))

            self.engine.step(steps, direction, STYLE)
            self._curLength = 0
        else:
            self.engine.step(unit, direction, STYLE)

    def retract_delta(self, centimeters):
        iterations = floor(centimeters)
        leftovers = int((centimeters - iterations) * 10) # in mm
        while iterations:
            self.retract_single(unit=Engine.STEPS_PER_CM)
            iterations -= 1
            self._curLength -= 1

        while leftovers:
            self.retract_single(unit=Engine.STEPS_PER_MM)
            leftovers -= 1
            self._curLength -= 0.1

    def expand_delta(self, centimeters):
        iterations = floor(centimeters)
        leftovers = int((centimeters - iterations) * 10) # in mm

        while iterations:
            self.expand_single(unit=Engine.STEPS_PER_CM)
            iterations -= 1
            self._curLength += 1

        while leftovers:
            self.expand_single(unit=Engine.STEPS_PER_MM)
            leftovers -= 1
            self._curLength += 0.1

class LeftEngine(Engine):

    def retract_single(self, unit=Engine.STEPS_PER_CM):
        self.towardsLowerBoundary(BACKWARD, unit)
        return self

    def expand_single(self, unit=Engine.STEPS_PER_CM):
        self.towardsUpperBoundary(FORWARD, unit)
        return self

class RightEngine(Engine):
    def retract_single(self, unit=Engine.STEPS_PER_CM):
        self.towardsLowerBoundary(FORWARD, unit)
        return self

    def expand_single(self, unit=Engine.STEPS_PER_CM):
        self.towardsUpperBoundary(BACKWARD, unit)
        return self

def fromInt(direction):
    if direction == FORWARD: return "FORWARD"
    if direction == BACKWARD: return "BACKWARD"
    return None