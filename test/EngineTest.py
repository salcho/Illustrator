import unittest
from Queue import Queue

from illustrator.Engine import Engine, LeftEngine, RightEngine

from TestClasses import TestHat


class EngineTest(unittest.TestCase):

    def test_validatesInitialPosition(self):
        with self.assertRaises(Exception):
            Engine("test", 1, TestHat(), -1, 1)

        with self.assertRaises(Exception):
            Engine("test", 1, TestHat(), 11, 10)

        try:
            LeftEngine("test", 1, TestHat(), 0, 1)
            RightEngine("test", 1, TestHat(), 0, 1)
        except:
            self.fail("Engine rejects initial position 0")

    def test_remembersPosition(self):
        self.assertEquals(LeftEngine("test", 1, TestHat(), 50, 100).expand(10).retract(10).currentPosition(), 50)
        self.assertEquals(RightEngine("test", 1, TestHat(), 50, 100).retract(10).currentPosition(), 40)
        self.assertRaises(LeftEngine("test", 1, TestHat(), 50, 100).retract(10).expand(50).currentPosition())

    def test_staysWithinLimits(self):
        # Moves to the closest boundary if delta is too big or too small
        self.assertRaises(StandardError, LeftEngine("test", 1, TestHat(), 5, 10).retract, args=5)
        self.assertRaises(StandardError, RightEngine("test", 1, TestHat(), 5, 10).retract(4).expand, args = 20)