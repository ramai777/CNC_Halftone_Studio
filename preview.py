import cv2
import numpy as np


class PreviewRenderer:

    def render(self, processor, holes):

        h, w = processor.get_gray().shape

        # Белый холст
        image = np.full((h, w, 3), 255, dtype=np.uint8)

        # Рисуем заполненные отверстия
        for hole in holes:

            radius = max(1, int(round(hole.diameter / 2)))

            cv2.circle(
                image,
                (int(hole.x), int(hole.y)),
                radius,
                (0, 0, 0),
                -1      # заполненный круг
            )

        return image