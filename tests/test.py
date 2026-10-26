from unittest.mock import Mock

from controller import Controller
from database import TriangleDatabase
from triangle import TriangleCalculator


def test_controller():
    user_interface = Mock()
    user_interface.get_input.return_value = ("3", "4", "5")

    external_service = Mock()

    controller = Controller(
        calculator=TriangleCalculator(),
        database=TriangleDatabase(":memory:"),
        user_interface=user_interface,
        external_service=external_service
    )

    result = controller.run()

    assert result["triangle_type"] == "разносторонний"
    external_service.send.assert_called_once()
