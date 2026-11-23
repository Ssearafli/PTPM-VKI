import unittest
from unittest.mock import Mock
from src.triangle import TriangleCalculator
from src.database import TriangleDatabase
from src.user_io import UserInterface, ConsoleUserInterface
from src.external_service import ExternalService, LoggingExternalService
from src.controller import TriangleController


class TestTriangleCalculatorUnit(unittest.TestCase):

    def test_equilateral(self):
        calc = TriangleCalculator()
        type, coords = calc.calculate_triangle("3", "3", "3")
        self.assertEqual(type, "равносторонний")
        self.assertEqual(len(coords), 3)

    def test_invalid_numbers(self):
        calc = TriangleCalculator()
        type, coords = calc.calculate_triangle("abc", "2", "2")
        self.assertEqual(type, "")
        self.assertEqual(coords[0], (-2, -2))


class TestDatabaseUnit(unittest.TestCase):
    def setUp(self):
        self.db = TriangleDatabase(":memory:")

    def tearDown(self):
        self.db.close()

    def test_add_get_delete(self):
        self.db.add_record("3", "3", "3", "равносторонний")
        rec = self.db.get_record("3", "3", "3")
        self.assertEqual(rec["triangle_type"], "равносторонний")
        self.db.delete_record("3", "3", "3")
        self.assertIsNone(self.db.get_record("3", "3", "3"))


class TestControllerIntegration(unittest.TestCase):
    def setUp(self):
        self.db = TriangleDatabase(":memory:")
        self.calc = TriangleCalculator()

    def tearDown(self):
        self.db.close()

    def _build_ui(self, values):
        ui = Mock(spec=UserInterface)
        ui.get_input.side_effect = values
        return ui

    def test_integration_new_data_computed_and_stored(self):
        # вычисление + запись + отправка
        ui = self._build_ui(["3", "3", "3"])
        external = Mock(spec=ExternalService)
        external.send.return_value = True

        controller = TriangleController(self.calc, self.db, ui, external)
        result, source = controller.process()

        self.assertEqual(source, "вычислено")
        self.assertIn("равносторонний", result)
        self.assertIsNotNone(self.db.get_record("3", "3", "3"))
        external.send.assert_called_once()

    def test_integration_existing_data_taken_from_db(self):
        #результат из БД, калькулятор не вызывается
        self.db.add_record("4", "4", "5", "равнобедренный")
        ui = self._build_ui(["4", "4", "5"])
        external = Mock(spec=ExternalService)
        external.send.return_value = True

        calc_spy = Mock(wraps=self.calc)
        controller = TriangleController(calc_spy, self.db, ui, external)
        result, source = controller.process()

        self.assertEqual(source, "из БД")
        self.assertIn("равнобедренный", result)
        calc_spy.calculate_triangle.assert_not_called()
        external.send.assert_called_once()

    def test_integration_full_scenario_with_real_logging_service(self):
        # все вместе
        ui = self._build_ui(["6", "6", "6"])
        external = LoggingExternalService()
        controller = TriangleController(self.calc, self.db, ui, external)

        result, source = controller.process()
        self.assertEqual(source, "вычислено")
        self.assertEqual(external.sent_messages, [result])

        ui2 = self._build_ui(["6", "6", "6"])
        controller2 = TriangleController(self.calc, self.db, ui2, external)
        result2, source2 = controller2.process()
        self.assertEqual(source2, "из БД")
        self.assertEqual(len(external.sent_messages), 2)

    def test_integration_external_service_mock_send_payload(self):
        ui = self._build_ui(["5", "5", "8"])
        external = Mock(spec=ExternalService)
        controller = TriangleController(self.calc, self.db, ui, external)

        result, _ = controller.process()
        self.assertIn("равнобедренный", result)
        external.send.assert_called_once_with(result)

if __name__ == "__main__":
    unittest.main()