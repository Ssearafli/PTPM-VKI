import logging

log_format = "%(asctime)s | [%(levelname)-7s] | %(message)s"
date_format = "%Y-%m-%d %H:%M:%S"

logging.basicConfig(
    level=logging.DEBUG,
    format=log_format,
    datefmt=date_format,
    handlers=[
        #logging.StreamHandler(),
        logging.FileHandler(
            "file_txt.log",
            encoding="utf-8"
        )
    ]
)

logger = logging.getLogger(__name__)

logger.info("Логгер успешно сконфигурирован")
logging.info("Логгер успешно сконфигурирован")
logger.info("Приложение запущено")


def is_valid_number(value):
    return value == value and abs(value) != float("inf")


def calculate_triangle(side_a_text, side_b_text, side_c_text):
    parameters = {
        "A": side_a_text,
        "B": side_b_text,
        "C": side_c_text
    }

    logger.info(
        "Начало обработки запроса: параметры=%s",
        parameters
    )

    try:
        a = float(side_a_text)
        b = float(side_b_text)
        c = float(side_c_text)

    except (TypeError, ValueError) as error:
        logger.error(
            "Нечисловые данные: параметры=%s, ошибка=%s",
            parameters,
            error,
            exc_info=True
        )

        return "", [
            (-2, -2),
            (-2, -2),
            (-2, -2)
        ]

    if (
        not is_valid_number(a)
        or not is_valid_number(b)
        or not is_valid_number(c)
        or a <= 0
        or b <= 0
        or c <= 0
    ):
        error_message = (
            "Стороны должны быть конечными положительными числами"
        )

        logger.error(
            "Ошибочные числовые данные: параметры=%s, ошибка=%s",
            parameters,
            error_message,
            exc_info=True
        )

        return "", [
            (-1, -1),
            (-1, -1),
            (-1, -1)
        ]

    if a + b <= c or a + c <= b or b + c <= a:
        logger.info(
            "Фигура не является треугольником: параметры=%s",
            parameters
        )

        return "не треугольник", [
            (-1, -1),
            (-1, -1),
            (-1, -1)
        ]

    if a==b and a==c:
        triangle_type = "равносторонний"
    elif a==b or a==c or b==c:
        triangle_type = "равнобедренный"
    else:
        triangle_type = "разносторонний"

    try:

        x_a = 0.0
        y_a = 0.0

        x_b = c
        y_b = 0.0

        x_c = (a * a + c * c - b * b) / (2 * c)

        y_c_squared = a * a - x_c * x_c

        if y_c_squared < 0 and y_c_squared > -1e-6:
            y_c_squared = 0.0

        if y_c_squared < 0:
            raise ValueError(
                "Невозможно вычислить координаты вершины"
            )

        y_c = y_c_squared ** 0.5

        raw_points = [
            (x_a, y_a),
            (x_b, y_b),
            (x_c, y_c)
        ]

        margin = 5.0
        available_size = 90.0

        min_x = min(point[0] for point in raw_points)
        max_x = max(point[0] for point in raw_points)

        min_y = min(point[1] for point in raw_points)
        max_y = max(point[1] for point in raw_points)

        width = max_x - min_x
        height = max_y - min_y

        if width == 0 or height == 0:
            raise ValueError(
                "Нулевая ширина или высота треугольника"
            )

        scale = min(
            available_size / width,
            available_size / height
        )

        coordinates = []

        for x, y in raw_points:
            pixel_x = round(
                margin + (x - min_x) * scale
            )

            pixel_y = round(
                margin + (max_y - y) * scale
            )

            pixel_x = max(0, min(99, pixel_x))
            pixel_y = max(0, min(99, pixel_y))

            coordinates.append((pixel_x, pixel_y))

        logger.info(
            "Успешный запрос: тип=%s, координаты=%s",
            triangle_type,
            coordinates
        )

        return triangle_type, coordinates

    except Exception as error:
        logger.error(
            "Ошибка вычисления координат: параметры=%s, ошибка=%s",
            parameters,
            error,
            exc_info=True
        )

        return "", [
            (-1, -1),
            (-1, -1),
            (-1, -1)
        ]


if __name__ == "__main__":
    side_a = input().strip()
    side_b = input().strip()
    side_c = input().strip()

    triangle_type, coordinates = calculate_triangle(side_a, side_b, side_c)
    print(triangle_type)
    print(coordinates)