import unittest
from Queue import Queue

from illustrator.Engine import Engine, LeftEngine, RightEngine

from backup.test import TestHat


class EngineTest(unittest.TestCase):

    def test_validatesInitialPosition(self):
        with self.assertRaises(Exception):
            Engine("test", 1, TestHat(), -1, 1, Queue())

        with self.assertRaises(Exception):
            Engine("test", 1, TestHat(), 11, 10, Queue())

        try:
            LeftEngine("test", 1, TestHat(), 0, 1, Queue())
            RightEngine("test", 1, TestHat(), 0, 1, Queue())
        except:
            self.fail("Engine rejects initial position 0")

    def test_remembersPosition(self):
        self.assertEquals(LeftEngine("test", 1, TestHat(), 0, 100, Queue()).retract(100).expand(100).currentPosition(), 100)
        self.assertEquals(RightEngine("test", 1, TestHat(), 0, 100, Queue()).retract(100).currentPosition(), 0)
        self.assertEquals(LeftEngine("test", 1, TestHat(), 0, 100, Queue()).retract(100).expand(50).currentPosition(), 50)

    def test_staysWithinLimits(self):
        # Moves to the closest boundary if delta is too big or too small
        self.assertEquals(LeftEngine("test", 1, TestHat(), 0, 10, Queue()).retract(10).retract(10).currentPosition(), 0)
        self.assertEquals(RightEngine("test", 1, TestHat(), 0, 10, Queue()).retract(5).expand(20).currentPosition(), 10)