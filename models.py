from dataclasses import dataclass


@dataclass
class Hole:
    """
    Одно отверстие будущего DXF
    """

    x: float
    y: float
    diameter: float
    brightness: int