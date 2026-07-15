from dataclasses import dataclass
import math


@dataclass
class Point:
    x: float
    y: float


@dataclass
class Hole:
    x: float
    y: float
    diameter: float
    depth: float
    brightness: int


def distance(p1: Point, p2: Point) -> float:
    """Расстояние между двумя точками"""
    return math.hypot(p2.x - p1.x, p2.y - p1.y)


def diameter_to_depth(diameter: float, tip_diameter: float = 0.5) -> float:
    """
    Расчет глубины для V-Bit 90°
    depth = (D - d_tip) / 2
    """
    if diameter <= tip_diameter:
        return 0.0

    return (diameter - tip_diameter) / 2


def mm_to_px(mm: float, pixels: int, size_mm: float) -> float:
    """Перевод миллиметров в пиксели"""
    return mm * pixels / size_mm


def px_to_mm(px: float, pixels: int, size_mm: float) -> float:
    """Перевод пикселей в миллиметры"""
    return px * size_mm / pixels