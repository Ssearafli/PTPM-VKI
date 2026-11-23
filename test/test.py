import unittest
from src.project import Converter


class TestConverter(unittest.TestCase):
    def test_values_at_or_above_upper_limit(self):
        self.assertEqual(Converter.do(100.7), 1000)
        self.assertEqual(Converter.do(100.8), 1000)
        self.assertEqual(Converter.do(150.0), 1000)

    def test_positive_values_below_upper_limit(self):
        self.assertEqual(Converter.do(0.1), 0)
        self.assertEqual(Converter.do(65.7), 65)
        self.assertEqual(Converter.do(100.6), 100)

    def test_zero_raises_value_error(self):
        with self.assertRaises(ValueError):
            Converter.do(0.0)

    def test_negative_values_in_middle_range(self):
        self.assertEqual(Converter.do(-0.1), -5)
        self.assertEqual(Converter.do(-12.7), -17)
        self.assertEqual(Converter.do(-30.4), -35)

    def test_values_at_or_below_lower_limit(self):
        self.assertEqual(Converter.do(-30.5), -2000)
        self.assertEqual(Converter.do(-30.6), -2000)
        self.assertEqual(Converter.do(-100.0), -2000)


if __name__ == "__main__":
    unittest.main()
