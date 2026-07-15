import math

from geometry import Hole, diameter_to_depth
from hexgrid import HexGridGenerator
from sampling import BrightnessSampler


class HalftoneGenerator:

    def __init__(
        self,
        min_diameter=1.0,
        max_diameter=4.0,
        bridge=2.5,
    ):
        self.min_diameter = min_diameter
        self.max_diameter = max_diameter
        self.bridge = bridge

        self.holes = []

    def clear(self):
        self.holes.clear()

    def generate(self, processor):

        self.clear()

        width = processor.width()
        height = processor.height()

        # Шаг между центрами отверстий
        step = self.max_diameter + self.bridge

        row = 0
        y = 0.0

        while y < height:

            if row % 2 == 0:
                x = 0.0
            else:
                x = step / 2

            while x < width:

                brightness = processor.brightness(int(x), int(y))

                # 255 = белый
                # 0 = черный

                diameter = self.min_diameter + (
                    brightness / 255
                ) * (
                    self.max_diameter - self.min_diameter
                )

                self.holes.append(
                    Hole(
                        x=x,
                        y=y,
                        diameter=diameter,
                        brightness=brightness,
                    )
                )

                x += step

            y += step * math.sqrt(3) / 2
            row += 1

        return self.holes