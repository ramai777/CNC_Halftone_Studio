from geometry import diameter_to_depth


def brightness_to_diameter(
    brightness: float,
    min_diameter: float,
    max_diameter: float,
    gamma: float,
) -> float:
    """
    Перевод яркости изображения в диаметр отверстия.

    brightness:
        0   = черный
        255 = белый
    """

    normalized = 1.0 - brightness / 255.0

    normalized = max(0.0, min(1.0, normalized))

    value = normalized ** gamma

    return min_diameter + (
        max_diameter - min_diameter
    ) * value


def diameter_to_hole_depth(
    diameter: float,
    tip_diameter: float,
):
    return diameter_to_depth(
        diameter,
        tip_diameter,
    )