from backup.illustrator.IHat import IHat

class TestHat(IHat):
    def getMotor(self, id):
        return TestStepper()

    def getStepper(self, steps, id):
        return TestStepper()


class TestStepper(object):
    def step(self, idx, direction, style):
        pass
    def run(self, action):
        pass
    def setSpeed(self, speed):
        pass