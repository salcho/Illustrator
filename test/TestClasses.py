from illustrator.IHat import IHat


class TestHat(IHat):
    def __init__(self):
        self.motorCount = 0
        self.stepper = TestStepper()

    def getMotor(self, id):
        return self.stepper

    def getStepper(self, steps, id):
        return self.stepper


class TestStepper(object):
    def __init__(self):
        self.stepSequence = []

    def step(self, idx, direction, style):
        self.stepSequence.append((idx, direction, style))

    def run(self, action):
        pass

    def setSpeed(self, speed):
        pass
