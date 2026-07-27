import cv2
import numpy as np


class PreviewRenderer:

    def render(self, processor, holes):

        h, w = processor.get_gray().shape

        image = np.full((h, w, 3), 220, dtype=np.uint8)

        pixels_per_mm = processor.width() / 450  # временно

        for hole in holes:

            radius = max(
                1,
                int(round(hole.diameter * pixels_per_mm / 2))
            )

            x = int(round(hole.x * pixels_per_mm))
            y = int(round(hole.y * pixels_per_mm))

            # Светлый ободок
            cv2.circle(
                image,
                (x, y),
                radius + 1,
                (180, 180, 180),
                -1
            )

            # Само отверстие
            cv2.circle(
                image,
                (x, y),
                radius,
                (35, 35, 35),
                -1
            )

        return image