import unittest
from src.Lab_1 import calculate_triangle

class TypeTriangle(unittest.TestCase):
    def test_isosceles_triangle(self):
        triangle_type, coordinates = calculate_triangle("5", "5", "6")
        self.assertEqual(triangle_type,  "равнобедренный")
        
    def test_equal_sides_in_different_order_are_isosceles(self):
        triangle_type, coordinates = calculate_triangle("5", "6", "5")
        self.assertEqual(triangle_type, "равнобедренный")

    def test_last_two_equal_sides_are_isosceles(self):
        triangle_type, coordinates = calculate_triangle("6", "5", "5")
        self.assertEqual(triangle_type, "равнобедренный")
        
    def test_equilateral_triangle(self):
        triangle_type, coordinates = calculate_triangle("5", "5", "5")
        self.assertEqual(triangle_type,  "равносторонний")
    
    def test_versatile_triangle(self):
        triangle_type, coordinates = calculate_triangle("10","12","20")
        self.assertEqual(triangle_type, "разносторонний")
        
    def test_valid_triangle(self):
        triangle_type, coordinates = calculate_triangle("2", "3", "5")
        self.assertEqual(triangle_type, "не треугольник")

    def test_zero_side(self):
        triangle_type, coordinates = calculate_triangle("0", "5", "5")
        self.assertEqual(triangle_type, "")

    def test_negative_side(self):
        triangle_type, coordinates = calculate_triangle("-3", "5", "5")
        self.assertEqual(triangle_type, "")

    def test_not_number(self):
        triangle_type, coordinates = calculate_triangle("abc", "5", "5")
        self.assertEqual(triangle_type, "")

    def test_empty_side(self):
        triangle_type, coordinates = calculate_triangle("", "5", "5")
        self.assertEqual(triangle_type, "")

    def test_nan_side(self):
        triangle_type, coordinates = calculate_triangle("nan", "5", "5")
        self.assertEqual(triangle_type, "")

    def test_infinite_side(self):
        triangle_type, coordinates = calculate_triangle("inf", "5", "5")
        self.assertEqual(triangle_type, "")
        
class Coordinates(unittest.TestCase):
    def test_quantity_coordinates(self):
        triangle_type, coordinates = calculate_triangle("5", "5", "6")
        self.assertEqual(len(coordinates), 3)
    
    def test_returns_error_coordinates_with_zero(self):
        triangle_type, coordinates = calculate_triangle("0", "5", "5")
        self.assertEqual(coordinates, [(-1, -1), (-1, -1), (-1, -1)])
    
    def test_returns_error_coordinates_with_negative_number(self):
        triangle_type, coordinates = calculate_triangle("-1", "5", "5")
        self.assertEqual(coordinates, [(-1, -1), (-1, -1), (-1, -1)])
            
    def test_returns_error_coordinates_not_triangle(self):
        triangle_type, coordinates = calculate_triangle("2", "3", "5")
        self.assertEqual(coordinates, [(-1, -1), (-1, -1), (-1, -1)])
        
    def test_another_error_coordinates_with_not_number(self):
        triangle_type, coordinates = calculate_triangle("abc", "5", "5")
        self.assertEqual(coordinates, [(-2, -2), (-2, -2), (-2, -2)])
    