import sys
import unittest

from illustrator.Engine import Engine
from illustrator.Illustrator import Illustrator, triangleLengths, cartesianCoords, areClose

from backup.test import TestHat


class IllustratorTest(unittest.TestCase):


    def setUp(self):
        self.testIllustrator = Illustrator(TestHat(), 10, 10, [1, 1],
                                           [Illustrator.MOTOR_DISTANCE + 2, Illustrator.MOTOR_DISTANCE + 2])

    def test_validatesArguments(self):
        # HAT
        with self.assertRaises(Exception):
            Illustrator(None, 1, 1, [1, 1], [1, 1])
        # canvas width
        with self.assertRaises(Exception):
            Illustrator(TestHat(), 0, 10, [1, 1], [1, 1])
        # canvas height
        with self.assertRaises(Exception):
            Illustrator(TestHat(), 10, 0, [1, 1], [1, 1])
        # 0 initial position
        with self.assertRaises(Exception):
            Illustrator(TestHat(), 10, 1, [0, 1], [1, 1])
        with self.assertRaises(Exception):
            Illustrator(TestHat(), 10, 1, [1, 0], [1, 1])
        # belt lengths insufficient
        with self.assertRaises(Exception):
            Illustrator(TestHat(), 1, 1, [1, 1], [Illustrator.MOTOR_DISTANCE/2, Illustrator.MOTOR_DISTANCE/2])


    def test_convertsToValidTriangleLengths(self):
        invalidLengths = [[-1,1], [1,-1], [-1,-1], [Illustrator.MOTOR_DISTANCE + 1, 1]]
        assertInvalidCases(invalidLengths, triangleLengths)

        invalidLengths = [[0,0], [-1,1], [1, -1], [-1, -1], [Illustrator.MOTOR_DISTANCE/2, Illustrator.MOTOR_DISTANCE/2]]
        assertInvalidCases(invalidLengths, cartesianCoords)

        coordinates = (float(Illustrator.MOTOR_DISTANCE/2), float(Illustrator.MOTOR_DISTANCE))
        assertClose(cartesianCoords(triangleLengths(coordinates)), coordinates)
        assertClose(triangleLengths(cartesianCoords(coordinates)), coordinates)
        assertClose(cartesianCoords(triangleLengths(cartesianCoords(triangleLengths(coordinates)))), coordinates)

    def test_goesHome(self):
            self.assertEquals(Illustrator(TestHat(), 1, 1, [1, 1], [sys.maxint, sys.maxint])
                                .start(findHome = True)
                                .currentPosition(),
                              (0, 0))
            self.assertNotEquals(Illustrator(TestHat(), 1, 1, [1, 1], [sys.maxint, sys.maxint])
                                .start()
                                .currentPosition(),
                              (1, 1))
            # Default option
            self.assertNotEquals(Illustrator(TestHat(), 1, 1, [1, 1], [sys.maxint, sys.maxint])
                                .start(findHome = False)
                                .currentPosition(),
                              (1, 1))

    def test_findsStraightLine(self):
        self.assertEquals(self.testIllustrator.findStraightLineTo(0, 0), (1, 0))
        self.assertEquals(self.testIllustrator.findStraightLineTo(1, 0), (None, None)) # Vertical movement
        self.assertEquals(self.testIllustrator.findStraightLineTo(2, 0), (-1, 2))
        self.assertEquals(self.testIllustrator.findStraightLineTo(2, 1), (0, 1)) # zero - horizontal

        self.assertEquals(self.testIllustrator.findStraightLineTo(2, 2), (1, 0))
        self.assertEquals(self.testIllustrator.findStraightLineTo(1, 2), (None, None))
        self.assertEquals(self.testIllustrator.findStraightLineTo(0, 2), (-1, 2))
        self.assertEquals(self.testIllustrator.findStraightLineTo(0, 1), (0, 1))

    def test_picksUpJobsFromQueue(self):
        illustrator = Illustrator(TestHat(), 10, 10, (1, 1), [Illustrator.MOTOR_DISTANCE + 2, Illustrator.MOTOR_DISTANCE + 2])
        illustrator.go(10, 10)
        self.assertEquals(illustrator.currentPosition(), (10, 10))

    def test(self):
        Engine.DEBUG = 0
        illustrator = Illustrator(TestHat(), 30, 30, (0, 0), (50,50))
        self.assertEquals(illustrator._currentPosition, (0, 0))
        self.assertEquals(illustrator.leftEngine._curPosition, 0)
        self.assertEquals(illustrator.rightEngine._curPosition, 0)
        illustrator.go(1, 1)

        #self.assertEquals(illustrator.currentPosition(), (10, 10))

def assertClose(x, y,):
    if len(x) != len(y): raise Exception("Different array lengths: (%d, %d)" % (len(x), len(y)))
    for i, a in enumerate(x):
        b = y[i]
        if not areClose(a, b): raise AssertionError("Not close: %d -> %d" % (a, b))
    return True

def assertInvalidCases(invalidCases, func):
    for invalidCase in invalidCases:
            try:
                func(invalidCase)
            except:
                continue
            raise AssertionError("Exception not raised for values: %s" % invalidCase)