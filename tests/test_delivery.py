import unittest
from src.Delivery import calculate_delivery_cost

class DeliveryCost(unittest.TestCase):
    def test_cost_for_default_package(self):
        cost, delivery_date = calculate_delivery_cost(1.0, 100, "обычный")
        self.assertEqual(cost, 700)
        
    def test_weight_at_five_kg(self):
        cost, delivery_date = calculate_delivery_cost(5.0, 100, "обычный")
        self.assertEqual(cost, 700)
        
    def test_weight_above_five_kg(self):
        cost, delivery_date = calculate_delivery_cost(6.0, 100, "обычный")
        self.assertEqual(cost, 840)
    
    def test_weight_below_twenty_kg(self):
        cost, delivery_date = calculate_delivery_cost(19.99, 100, "обычный")
        self.assertEqual(cost, 840)
    
    def test_weight_twenty_kg(self):
        cost, delivery_date = calculate_delivery_cost(20.0, 100, "обычный")
        self.assertEqual(cost, 1050)
        
    def test_weight_above_twenty_kg(self):
        cost, delivery_date = calculate_delivery_cost(21.0, 100, "обычный")
        self.assertEqual(cost, 1050)  
        
    def test_fragile_package(self):
        cost, delivery_date = calculate_delivery_cost(1.0, 100, "хрупкий")
        self.assertEqual(cost, 1000)

    def test_dangerous_package(self):
        cost, delivery_date = calculate_delivery_cost(1.0, 100, "опасный")
        self.assertEqual(cost, 1700)
        
    def test_applies_express_discount(self):
        cost, delivery_date = calculate_delivery_cost(1.0, 100, "обычный", is_express=True)
        self.assertEqual(cost, 1400)
    
    def test_distante(self):
        cost, delivery_date = calculate_delivery_cost(1.0, 3000, "обычный")
        self.assertEqual(cost, 15200)
        
class InputValidation(unittest.TestCase):
    def test_weight_below_minimum(self):
        result = calculate_delivery_cost(0, 100, "обычный")
        self.assertEqual(result, (-1, "0000-00-00"))

    def test_weight_above_maximum(self):
        result = calculate_delivery_cost(60.0, 100, "обычный")
        self.assertEqual(result, (-1, "0000-00-00"))

    def test_distance_below_minimum(self):
        result = calculate_delivery_cost(1.0, 0, "обычный")
        self.assertEqual(result, (-1, "0000-00-00"))

    def test_distance_above_maximum(self):
        result = calculate_delivery_cost(1.0, 6000, "обычный")
        self.assertEqual(result, (-1, "0000-00-00"))

    def test_unknown_package_type(self):
        result = calculate_delivery_cost(1.0, 100, "нестандартный")
        self.assertEqual(result, (-1, "0000-00-00"))
        
class DeliveryTime(unittest.TestCase):
    def test_delivery_takes_one_day_for_short_distance(self):
        cost, delivery_date = calculate_delivery_cost(1.0, 500, "обычный")
        self.assertEqual(delivery_date, "2026-09-04")

    def test_delivery_takes_two_days_at_one_thousand_km(self):
        cost, delivery_date = calculate_delivery_cost(1.0, 1000, "обычный")
        self.assertEqual(delivery_date, "2026-09-05")

    def test_express_delivery_takes_at_least_one_day(self):
        cost, delivery_date = calculate_delivery_cost(1.0, 100, "обычный", is_express=True)
        self.assertEqual(delivery_date, "2026-09-04")

    def test_express_delivery_halves_days_at_two_thousand_km(self):
        cost, delivery_date = calculate_delivery_cost(1.0, 2000, "обычный", is_express=True)
        self.assertEqual(delivery_date, "2026-09-05")