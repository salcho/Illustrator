import unittest
from Queue import Queue

from illustrator.Engine import Engine, LeftEngine, RightEngine

from TestClasses import TestHat


class EngineTest(unittest.TestCase):
    def test_validatesInitialPosition(self):
        with self.assertRaises(Exception):
            Engine("test", 1, TestHat(), -1, beltLength=1, instructionQueue=null)

        with self.assertRaises(Exception):
            Engine("test", 1, TestHat(), 11, beltLength=10, instructionQueue=null)

        try:
            LeftEngine("test", 1, TestHat(), 0, 1)
            RightEngine("test", 1, TestHat(), 0, 1)
        except:
            self.fail("Engine rejects initial position 0")

    def test_remembersPosition(self):
        self.assertEquals(LeftEngine("test", 1, TestHat(), 50, 100, Queue()).expand(10).retract(10).currentLength(), 50)
        self.assertEquals(RightEngine("test", 1, TestHat(), 50, 100, Queue()).retract(10).currentLength(), 40)
        self.assertEquals(LeftEngine("test", 1, TestHat(), 50, 100, Queue()).retract(10).expand(50).currentLength(), 90)

    def test_staysWithinLimits(self):
        # Moves to the closest boundary if delta overflows
        self.assertEquals(LeftEngine("test", 1, TestHat(), 5, 10, Queue()).retract(5).currentLength(), 0)
        self.assertEquals(LeftEngine("test", 1, TestHat(), 5, 10, Queue()).retract(10).currentLength(), 0)
        self.assertEquals(RightEngine("test", 1, TestHat(), 5, 10, Queue()).retract(4).expand(9).currentLength(), 10)
        self.assertEquals(RightEngine("test", 1, TestHat(), 5, 10, Queue()).retract(4).expand(20).currentLength(), 10)
