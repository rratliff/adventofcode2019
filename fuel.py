import math
import unittest

def getFuel(mass):
    return math.floor(mass/3) - 2

class TestFuelCalculation(unittest.TestCase):

    def test_examples(self):
        self.assertEqual(getFuel(12), 2)
        self.assertEqual(getFuel(14), 2)
        self.assertEqual(getFuel(1969), 654)
        self.assertEqual(getFuel(100756), 33583)

if __name__ == '__main__':
    unittest.main()
