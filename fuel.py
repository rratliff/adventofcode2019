import math
import unittest

def getFuel(mass):
    if _getFuelNaive(mass) <= 0:
        return 0
    else:
        return _getFuelNaive(mass) + getFuel(_getFuelNaive(mass))

def _getFuelNaive(mass):
    return math.floor(mass/3) - 2

class TestFuelCalculation(unittest.TestCase):

    def test_getFuelNaive(self):
        self.assertEqual(_getFuelNaive(12), 2)
        self.assertEqual(_getFuelNaive(14), 2)
        self.assertEqual(_getFuelNaive(1969), 654)
        self.assertEqual(_getFuelNaive(100756), 33583)

    def test_getFuel(self):
        self.assertEqual(getFuel(14), 2)
        self.assertEqual(getFuel(1969), 966)
        self.assertEqual(getFuel(100756), 50346)

if __name__ == '__main__':
    unittest.main()
