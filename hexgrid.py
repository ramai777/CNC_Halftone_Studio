import math
from geometry import Point


class HexGridGenerator:
    """
    Генератор шестиугольной сетки в миллиметрах.
    """

    def __init__(self):
        pass

    def generate(
        self,
        width_mm,
        height_mm,
        grid_step
    ):
        """
        Возвращает список точек центров отверстий.
        """

        points = []

        # Расстояние между центрами отверстий
        step = grid_step

        # Высота шестиугольной сетки
        row_height = step * math.sqrt(3) / 2

        row = 0
        y = 0.0

        while y <= height_mm:

            if row % 2 == 0:
                x = 0.0
            else:
                x = step / 2

            while x <= width_mm:

                points.append(Point(x, y))

                x += step

            y += row_height
            row += 1

        return points