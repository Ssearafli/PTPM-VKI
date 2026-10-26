from controller import Controller
from database import TriangleDatabase
from external_interface import MockExternalService
from triangle import TriangleCalculator
from user_interface import ConsoleUserInterface


def main():
    controller = Controller(
        calculator=TriangleCalculator(),
        database=TriangleDatabase(),
        user_interface=ConsoleUserInterface(),
        external_service=MockExternalService()
    )

    result = controller.run()

    print(result["triangle_type"])
    print(result["coordinates"])

    if result["error_message"]:
        print(result["error_message"])


if __name__ == "__main__":
    main()
