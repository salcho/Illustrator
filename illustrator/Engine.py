from threading import Thread

from test.TestClasses import TestHat


class Engine(object):
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
            delta = self._curPosition - length
            thread = None
            if not delta:
                pass
            elif delta > 0:
                self.moveRight(delta)
            else:
                self.moveLeft(delta)
            print '[%s] Current position is: %d' % (self, self._curPosition)
            self.q.task_done()

    def moveRight(self, delta):
        if self._curPosition + delta > self._beltLength:
            self._curPosition = self._beltLength
            self.engine.step(self._beltLength - self._curPosition, Engine.forward, Engine.style)
        else:
            self._curPosition += delta
            self.engine.step(int(delta), Engine.forward, Engine.style)
        return self

    def moveLeft(self, delta):
        if self._curPosition - delta < 0:
            self._curPosition = 0
            self.engine.step(self._curPosition, Engine.backward, Engine.style)
        else:
            self._curPosition -= delta
            self.engine.step(int(delta), Engine.backward, Engine.style)

        return self

    def currentPosition(self):
        return self._curPosition
