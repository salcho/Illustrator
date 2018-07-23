import sys
import unittest
from math import ceil

from illustrator.Engine import Engine
from illustrator.Illustrator import Illustrator, CANVAS_DIMENSIONS
from illustrator.CartesianIllustrator import cartesianCoords, CartesianIllustrator

from TestClasses import TestHat


class IllustratorTest(unittest.TestCase):
    def setUp(self):
        self.testIllustrator = CartesianIllustrator(TestHat(), (10, 10), [1, 1], belt_lengths=[CANVAS_DIMENSIONS + 2, CANVAS_DIMENSIONS + 2])

    def tearDown(self):
        Engine.DEBUG = 1

    def test_validatesArguments(self):
        # HAT
        with self.assertRaises(Exception):
            CartesianIllustrator(None, canvasDimensions=(1, 1), initialPositions=[1, 1], belt_lengths=[1, 1])
        # canvas width
        with self.assertRaises(Exception):
            CartesianIllustrator(TestHat(), canvasDimensions=(0, 10), initialPositions=[1, 1], belt_lengths=[1, 1])
        # canvas height
        with self.assertRaises(Exception):
            CartesianIllustrator(TestHat(), canvasDimensions=(10, 0), initialPositions=[1, 1], belt_lengths=[1, 1])
        # belt lengths insufficient
        with self.assertRaises(Exception):
            CartesianIllustrator(TestHat(), canvasDimensions=(1, 1), initialPositions=[1, 1],
                                 belt_lengths=[CANVAS_DIMENSIONS / 3, CANVAS_DIMENSIONS / 3])

    def test_convertsToValidTriangleLengths(self):
        invalidLengths = [[-1, 1], [1, -1], [-1, -1], [CANVAS_DIMENSIONS + 1, 1]]
        assertInvalidCases(invalidLengths, self.testIllustrator.triangleLengths)

        invalidLengths = [[0, 0], [-1, 1], [1, -1], [-1, -1], [CANVAS_DIMENSIONS / 2, CANVAS_DIMENSIONS / 2]]
        assertInvalidCases(invalidLengths, cartesianCoords)

        coordinates = (float(CANVAS_DIMENSIONS / 2), float(CANVAS_DIMENSIONS))
        self.assertClose(cartesianCoords(self.testIllustrator.triangleLengths(coordinates)), coordinates)
        self.assertClose(self.testIllustrator.triangleLengths(cartesianCoords(coordinates)), coordinates)
        self.assertClose(cartesianCoords(
            self.testIllustrator.triangleLengths(cartesianCoords(self.testIllustrator.triangleLengths(coordinates)))),
                         coordinates)

    def test(self):
        illustrator = CartesianIllustrator(TestHat(), (CANVAS_DIMENSIONS, CANVAS_DIMENSIONS), (0, 0), belt_lengths=(60, 60))
        self.assertEquals(illustrator.currentPosition(), (0, 0))
        self.assertEquals(illustrator.leftEngine.currentLength(), 0)
        self.assertEquals(illustrator.rightEngine.currentLength(), CANVAS_DIMENSIONS)
        illustrator.go(10, 10)
        self.assertEquals(ceil(illustrator.leftEngine.currentLength()), 12)
        self.assertEquals(illustrator.rightEngine.currentLength(), 32)
        self.assertEquals(illustrator.currentPosition(), (10, 10))

    def test_goesHome(self):
        self.assertEquals(CartesianIllustrator(TestHat(), canvasDimensions=(1, 1), initialPositions=[1, 1],
                                               belt_lengths=[sys.maxint, sys.maxint])
                          .start(findHome=True)
                          .currentPosition(),
                          (0, 0))
        self.assertNotEquals(CartesianIllustrator(TestHat(), canvasDimensions=(1, 1), initialPositions=[1, 1],
                                                  belt_lengths=[sys.maxint, sys.maxint])
                             .start()
                             .currentPosition(),
                             (1, 1))
        # Default option
        self.assertNotEquals(CartesianIllustrator(TestHat(), canvasDimensions=(1, 1), initialPositions=[1, 1],
                                                  belt_lengths=[sys.maxint, sys.maxint])
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
        illustrator = CartesianIllustrator(TestHat(), (10, 10), (1, 1), [CANVAS_DIMENSIONS + 2, CANVAS_DIMENSIONS + 2])
        illustrator.go(10, 10)
        self.assertEquals(illustrator.currentPosition(), (10, 10))

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
