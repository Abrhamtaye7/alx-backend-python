import unittest
from simple_calculator import SimpleCalculator


class TestSimpleCalculator(unittest.TestCase):
    """Unit tests for the SimpleCalculator class."""

    def setUp(self):
        """Set up the calculator instance before each test."""
        self.calc = SimpleCalculator()

    # ------------------------------
    # ADDITION TESTS
    # ------------------------------
    def test_addition(self):
        self.assertEqual(self.calc.add(2, 3), 5)
        self.assertEqual(self.calc.add(-1, -5), -6)
        self.assertEqual(self.calc.add(-1, 5), 4)
        self.assertEqual(self.calc.add(0, 0), 0)

    # ------------------------------
    # SUBTRACTION TESTS
    # ------------------------------
    def test_subtraction(self):
        self.assertEqual(self.calc.subtract(10, 5), 5)
        self.assertEqual(self.calc.subtract(5, 10), -5)
        self.assertEqual(self.calc.subtract(-5, -2), -3)
        self.assertEqual(self.calc.subtract(0, 0), 0)

    # ------------------------------
    # MULTIPLICATION TESTS
    # ------------------------------
    def test_multiplication(self):
        self.assertEqual(self.calc.multiply(4, 3), 12)
        self.assertEqual(self.calc.multiply(-4, 3), -12)
        self.assertEqual(self.calc.multiply(0, 10), 0)

    # ------------------------------
    # DIVISION TESTS
    # ------------------------------
    def test_division(self):
        self.assertAlmostEqual(self.calc.divide(10, 2), 5.0)
        self.assertAlmostEqual(self.calc.divide(7, 2), 3.5)
        self.assertAlmostEqual(self.calc.divide(-9, 3), -3.0)

    def test_division_by_zero(self):
        self.assertIsNone(self.calc.divide(10, 0))
        self.assertIsNone(self.calc.divide(0, 0))


if __name__ == "__main__":
    unittest.main()
