class Controller:
    def __init__(self, calculator, database, user_interface,
                 external_service):
        self.calculator = calculator
        self.database = database
        self.user_interface = user_interface
        self.external_service = external_service

    @staticmethod
    def _get_error_message(triangle_type, coordinates):
        if triangle_type == "не треугольник":
            return "Введённые стороны не образуют треугольник"

        if triangle_type:
            return ""

        if coordinates == [(-2, -2), (-2, -2), (-2, -2)]:
            return "Нечисловые данные"

        return "Стороны должны быть конечными положительными числами"

    def run(self):
        side_a, side_b, side_c = self.user_interface.get_input()

        cached_result = self.database.get(side_a, side_b, side_c)

        if cached_result is None:
            triangle_type, coordinates = self.calculator.calculate_triangle(
                side_a,
                side_b,
                side_c
            )
            error_message = self._get_error_message(
                triangle_type,
                coordinates
            )

            self.database.add(
                side_a,
                side_b,
                side_c,
                triangle_type,
                error_message,
                coordinates
            )
        else:
            triangle_type = cached_result["triangle_type"]
            error_message = cached_result["error_message"]
            coordinates = cached_result["coordinates"]

        result = {
            "triangle_type": triangle_type,
            "error_message": error_message,
            "coordinates": coordinates
        }

        self.external_service.send(str(result))
        return result
