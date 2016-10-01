import unittest
from Queue import Queue

from illustrator.Engine import Engine
from test.TestClasses import TestHat


class EngineTest(unittest.TestCase):

    def test_validatesInitialPosition(self):
        with self.assertRaises(Exception):
            Engine("test", 1, TestHat(), -1, 1, Queue())

        with self.assertRaises(Exception):
            Engine("test", 1, TestHat(), 11, 10, Queue())

        try:
            Engine("test", 1, TestHat(), 0, 1, Queue())
        except:
            self.fail("Engine rejects initial position 0")

    def test_remembersPosition(self):
        self.assertEquals(Engine("test", 1, TestHat(), 0, 100, Queue()).moveRight(100).moveLeft(100).currentPosition(), 0)
        self.assertEquals(Engine("test", 1, TestHat(), 0, 100, Queue()).moveRight(100).currentPosition(), 100)
        self.assertEquals(Engine("test", 1, TestHat(), 0, 100, Queue()).moveRight(100).moveLeft(50).currentPosition(), 50)

    def test_staysWithinLimits(self):
        # Moves to the closest boundary if delta is too big or too small
        self.assertEquals(Engine("test", 1, TestHat(), 0, 10, Queue()).moveRight(10).moveRight(10).currentPosition(), 10)
        self.assertEquals(Engine("test", 1, TestHat(), 0, 10, Queue()).moveRight(5).moveLeft(10).currentPosition(), 0)
