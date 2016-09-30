from test.TestClasses import TestHat


class Engine(object):
    stepsPerPhase = 200
    forward = TestHat.FORWARD
    backward = TestHat.BACKWARD
    style = TestHat.SINGLE

    def __init__(self, id, hat, initialPosition, beltLength):
        if initialPosition < 0 or initialPosition > beltLength:
            raise Exception("Invalid initial position for engine %d" % id)
        self.motorHat = hat
        self.id = id
        self.engine = hat.getStepper(Engine.stepsPerPhase, id)
        self._curPosition = initialPosition
        self._beltLength = beltLength

    # TODO: Which is right, forward or backward?
    def moveRight(self, delta):
        if self._curPosition + delta > self._beltLength:
            self._curPosition = self._beltLength
            self.engine.step(self._beltLength - self._curPosition, Engine.forward, Engine.style)
        else:
            self._curPosition += delta
            self.engine.step(delta, Engine.forward, Engine.style)
        return self

    def moveLeft(self, delta):
        if self._curPosition - delta < 0:
            self._curPosition = 0
            self.engine.step(self._curPosition, Engine.backward, Engine.style)
        else:
            self._curPosition -= delta
            self.engine.step(delta, Engine.backward, Engine.style)

        return self

    def currentPosition(self):
        return self._curPosition
