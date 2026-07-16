from geometry import Hole
from geometry import diameter_to_depth

from hexgrid import HexGridGenerator
from sampling import BrightnessSampler

from calculations import brightness_to_diameter
from config import Settings


class HalftoneGenerator:

    def __init__(self, settings: Settings | None = None):

        self.settings = settings or Settings()

        self.grid = HexGridGenerator()

        self.holes = []

    def clear(self):
        self.holes.clear()

    def generate(self, processor):

        self.clear()

        sampler = BrightnessSampler(
            processor.get_gray()
        )

        points = self.grid.generate(
            processor.width(),
            processor.height(),
            self.settings.max_diameter,
            self.settings.bridge,
        )

        for point in points:

            brightness = sampler.sample(
                point.x,
                point.y,
            )

            diameter = brightness_to_diameter(
                brightness,
                self.settings.min_diameter,
                self.settings.max_diameter,
                self.settings.gamma,
            )

            depth = diameter_to_depth(
                diameter,
                self.settings.tip_diameter,
            )

            self.holes.append(
                Hole(
                    x=point.x,
                    y=point.y,
                    diameter=diameter,
                    depth=depth,
                    brightness=brightness,
                )
            )

        return self.holes