import math
import unittest
from calculator import evaluate_expression, convert_units, CalculatorError

class CalculatorTests(unittest.TestCase):
    def test_arithmetic(self):
        self.assertEqual(evaluate_expression("2 + 3 * 4"), 14)
    def test_functions_and_constants(self):
        self.assertAlmostEqual(evaluate_expression("sqrt(81) + sin(pi/2)"), 10)
    def test_power(self):
        self.assertEqual(evaluate_expression("2 ** 8"), 256)
    def test_reject_unsafe_code(self):
        with self.assertRaises(CalculatorError):
            evaluate_expression("__import__('os').system('echo unsafe')")
    def test_divide_by_zero(self):
        with self.assertRaises(CalculatorError):
            evaluate_expression("1 / 0")
    def test_temperature(self):
        self.assertAlmostEqual(convert_units(0, "C", "F", "Temperature"), 32)
    def test_length(self):
        self.assertAlmostEqual(convert_units(1, "km", "m", "Length"), 1000)

if __name__ == "__main__":
    unittest.main()
