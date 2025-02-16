import unittest
from calculateAttackValues import calculateHitCritChance, calculateMaxOfD6, calculateD20Percentage


class MyTestCase(unittest.TestCase):
    # Hit, Crit, Miss
    # Expected (10, 0, 0): .5, .05, .45
    # Expected (0, 0, 0): .95, .05, 0
    # Expected (20, 0, 0): 0, .05, .95
    # Expected (10, 3, 0): .5, .20, .30
    # Expected (0, 3, 0): .80, .20, 0
    # Expected (20, 3, 0): 0, .20, .80
    # Expected (10, 0, 1): .5, .175, .275
    def test_calculateHistCritChance(self):
        testValues(self, (.50, .05, .45), calculateHitCritChance(10, 0, 0))
        testValues(self, (.95, .05, .00),  calculateHitCritChance(0, 0, 0))
        testValues(self, (.00, .05, .95), calculateHitCritChance(20, 0, 0))
        testValues(self, (.50, .20, .30), calculateHitCritChance(10, 3, 0))
        testValues(self, (.80, .20, .0),  calculateHitCritChance(0, 3, 0))
        testValues(self, (.00, .20, .80), calculateHitCritChance(20, 3, 0))
        testValues(self, (60/120, 27/120, 33/120), calculateHitCritChance(10, 0, 1))
        testValues(self, (60/120, 45/120, 15/120), calculateHitCritChance(10, 3, 1))

        testValues(self, (360/720, 197/720, 163/720), calculateHitCritChance(10, 0, 2))
        testValues(self, (360/720, 305/720, 55/720), calculateHitCritChance(10, 3, 2))

        print("Success!")


    def test_calculateD20Percentage(self):
        testValues(self, (.50, .05, .45), calculateD20Percentage(10, 0))
        testValues(self, (.50, .20, .30), calculateD20Percentage(10, 3))
        testValues(self, (.40, .00, .60), calculateD20Percentage(10, -3))
        testValues(self, (.25, .05, .70), calculateD20Percentage(15, 0))
        testValues(self, (.25, .20, .55), calculateD20Percentage(15, 3))
        testValues(self, (.15, .00, .85), calculateD20Percentage(15, -3))
        # Should all hit
        testValues(self, (.95, .05, .0), calculateD20Percentage(1, 0))
        testValues(self, (.45, .55, .0), calculateD20Percentage(1, 10))
        testValues(self, (.80, .20, .0), calculateD20Percentage(1, 3))
        # Most should miss
        testValues(self, (.0, .05, .95), calculateD20Percentage(20, 00))
        testValues(self, (.0, .20, .80), calculateD20Percentage(20, 3))
        testValues(self, (.0, .55, .45), calculateD20Percentage(20, 10))
        testValues(self, (.0, .05, .95), calculateD20Percentage(25, 00))
        testValues(self, (.0, .20, .80), calculateD20Percentage(25, 3))
        testValues(self, (.0, .55, .45), calculateD20Percentage(25, 10))
        # Most Values Should work.
        testValues(self, (.85, .0, .15), calculateD20Percentage(1, -3))
        testValues(self, (.90, .0, .10), calculateD20Percentage(0, -3))
        testValues(self, (.95, .0, .05), calculateD20Percentage(-1, -3))

        # All Critical Hits
        testValues(self, (.00, 1.0, .00), calculateD20Percentage(1, 20))
        testValues(self, (.00, 1.0, .00), calculateD20Percentage(10, 20))
        testValues(self, (.00, 1.0, .00), calculateD20Percentage(20, 20))
        print("Success!")

    def test_calculateMaxOfD6(self):
        # For the first accuracy
        for x in range(1,7):
            self.assertAlmostEqual(1/6, calculateMaxOfD6(x, 1), places=6)

        # For the second accuracy
        for x in range(1, 7):
            self.assertAlmostEqual((2 * (x-1) + 1)/36, calculateMaxOfD6(x, 2), places=6)
        print("Success!")


def testValues(testCase: MyTestCase, values1, values2):
    testCase.assertAlmostEqual(len(values1), len(values2), places=6)

    for x in range(len(values1)):
        testCase.assertAlmostEqual(values1[x], values2[x], places=6)


if __name__ == '__main__':
    unittest.main()
