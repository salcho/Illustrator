import abc

class IHat(object):
    RELEASE = 1
    FORWARD = 2
    BACKWARD = 3
    SINGLE = 4
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def getMotor(self, id):
        raise NotImplemented("getMotor")

    @abc.abstractmethod
    def getStepper(self, steps, id):
        raise NotImplemented("getStepper")