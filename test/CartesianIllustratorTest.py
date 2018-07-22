import sys
import unittest

from illustrator.Engine import Engine
from illustrator.Illustrator import Illustrator, MOTOR_DISTANCE
from illustrator.CartesianIllustrator import cartesianCoords, CartesianIllustrator

from TestClasses import TestHat


class IllustratorTest(unittest.TestCase):
    def setUp(self):
        self.testIllustrator = CartesianIllustrator(TestHat(), (10, 10), [1, 1],
                                                    [MOTOR_DISTANCE + 2, MOTOR_DISTANCE + 2])

    def tearDown(self):
        Engine.DEBUG = 1

    def test_validatesArguments(self):
        # HAT
        with self.assertRaises(Exception):
            CartesianIllustrator(None, canvasDimensions=(1, 1), initialPositions=[1, 1], beltLengths=[1, 1])
        # canvas width
        with self.assertRaises(Exception):
            CartesianIllustrator(TestHat(), canvasDimensions=(0, 10), initialPositions=[1, 1], beltLengths=[1, 1])
        # canvas height
        with self.assertRaises(Exception):
            CartesianIllustrator(TestHat(), canvasDimensions=(10, 0), initialPositions=[1, 1], beltLengths=[1, 1])
        # belt lengths insufficient
        with self.assertRaises(Exception):
            CartesianIllustrator(TestHat(), canvasDimensions=(1, 1), initialPositions=[1, 1],
                                 beltLengths=[MOTOR_DISTANCE / 3, MOTOR_DISTANCE / 3])

    def test_convertsToValidTriangleLengths(self):
        invalidLengths = [[-1, 1], [1, -1], [-1, -1], [MOTOR_DISTANCE + 1, 1]]
        assertInvalidCases(invalidLengths, self.testIllustrator.triangleLengths)

        invalidLengths = [[0, 0], [-1, 1], [1, -1], [-1, -1], [MOTOR_DISTANCE / 2, MOTOR_DISTANCE / 2]]
        assertInvalidCases(invalidLengths, cartesianCoords)

        coordinates = (float(MOTOR_DISTANCE / 2), float(MOTOR_DISTANCE))
        self.assertClose(cartesianCoords(self.testIllustrator.triangleLengths(coordinates)), coordinates)
        self.assertClose(self.testIllustrator.triangleLengths(cartesianCoords(coordinates)), coordinates)
        self.assertClose(cartesianCoords(
            self.testIllustrator.triangleLengths(cartesianCoords(self.testIllustrator.triangleLengths(coordinates)))),
                         coordinates)

    def test_goesHome(self):
        self.assertEquals(CartesianIllustrator(TestHat(), canvasDimensions=(1, 1), initialPositions=[1, 1],
                                               beltLengths=[sys.maxint, sys.maxint])
                          .start(findHome=True)
                          .currentPosition(),
                          (0, 0))
        self.assertNotEquals(CartesianIllustrator(TestHat(), canvasDimensions=(1, 1), initialPositions=[1, 1],
                                                  beltLengths=[sys.maxint, sys.maxint])
                             .start()
                             .currentPosition(),
                             (1, 1))
        # Default option
        self.assertNotEquals(CartesianIllustrator(TestHat(), canvasDimensions=(1, 1), initialPositions=[1, 1],
                                                  beltLengths=[sys.maxint, sys.maxint])
                             .start()
                             .currentPosition(),
                             (1, 1))

    def test_findsStraightLine(self):
        self.assertEquals(self.testIllustrator.findStraightLineTo(0, 0), (1, 0))
        self.assertEquals(self.testIllustrator.findStraightLineTo(1, 0), (None, None))  # Vertical movement
        self.assertEquals(self.testIllustrator.findStraightLineTo(2, 0), (-1, 2))
        self.assertEquals(self.testIllustrator.findStraightLineTo(2, 1), (0, 1))  # zero - horizontal

        self.assertEquals(self.testIllustrator.findStraightLineTo(2, 2), (1, 0))
        self.assertEquals(self.testIllustrator.findStraightLineTo(1, 2), (None, None))
        self.assertEquals(self.testIllustrator.findStraightLineTo(0, 2), (-1, 2))
        self.assertEquals(self.testIllustrator.findStraightLineTo(0, 1), (0, 1))

    def test_picksUpJobsFromQueue(self):
        illustrator = CartesianIllustrator(TestHat(), (10, 10), (1, 1), [MOTOR_DISTANCE + 2, MOTOR_DISTANCE + 2])
        illustrator.go(10, 10)
        self.assertEquals(illustrator.currentPosition(), (10, 10))

    def test(self):
        hat = TestHat()
        illustrator = CartesianIllustrator(hat, (30, 30), (20, 20), (50, 50))
        illustrator.go(10, 10)
        print hat.stepper.stepSequence

    def assertClose(self, x, y):
        if len(x) != len(y): raise Exception("Different array lengths: (%d, %d)" % (len(x), len(y)))
        for i, a in enumerate(x):
            b = y[i]
            if not self.testIllustrator.areClose(a, b): raise AssertionError("Not close: %d -> %d" % (a, b))
        return True


def assertInvalidCases(invalidCases, func):
    for invalidCase in invalidCases:
        try:
            func(invalidCase)
        except:
            continue
        raise AssertionError("Exception not raised for values: %s" % invalidCase)
