class TriangleController:
    def __init__(self, calculator, database, user_interface, external_service):
        self.calculator = calculator
        self.database = database
        self.ui = user_interface
        self.external = external_service

    def process(self):
        a = self.ui.get_input("Введите сторону A: ").strip()
        b = self.ui.get_input("Введите сторону B: ").strip()
        c = self.ui.get_input("Введите сторону C: ").strip()

        record = self.database.get_record(a, b, c)

        if record is None:
            triangle_type, coords = self.calculator.calculate_triangle(a, b, c)
            error_message = ""
            if triangle_type == "" or triangle_type == "не треугольник":
                error_message = "" if triangle_type == "не треугольник" else "ошибка вычисления"
            self.database.add_record(a, b, c, triangle_type, error_message)
            source = "вычислено"
        else:
            triangle_type = record["triangle_type"]
            source = "из БД"

        result_str = f"Тип: {triangle_type}"
        self.external.send(result_str)
        self.ui.show_result(result_str)
        return result_str, source