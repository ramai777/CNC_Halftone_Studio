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

        print("Старт генерации")

        self.clear()

        sampler = BrightnessSampler(
            processor.get_gray()
        )

        px_per_mm_x = processor.width() / self.settings.panel_width_mm
        px_per_mm_y = processor.height() / self.settings.panel_height_mm

        points = self.grid.generate(
            self.settings.panel_width_mm,
            self.settings.panel_height_mm,
            self.settings.grid_step,
        )
        print("Точек:", len(points))
        scale = self.settings.image_scale

        offset_x = self.settings.offset_x_mm
        offset_y = self.settings.offset_y_mm

        i = 0

        for point in points:

            i += 1

            if i % 1000 == 0:
                print(i)

            sample_x = (
                (point.x + offset_x)
                * scale
                * px_per_mm_x
            )

            sample_y = (
                (point.y + offset_y)
                * scale
                * px_per_mm_y
            )

            brightness = sampler.sample(
                sample_x,
                sample_y,
                self.settings.max_diameter * px_per_mm_x * scale
            )

            contrast = sampler.contrast(
                sample_x,
                sample_y
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
