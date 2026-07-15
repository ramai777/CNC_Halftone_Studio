import cv2
import numpy as np


class PreviewRenderer:

    def render(self, processor, holes):

        image = cv2.cvtColor(
            processor.get_gray(),
            cv2.COLOR_GRAY2BGR
        )

        for hole in holes:

            cv2.circle(
                image,
                (int(hole.x), int(hole.y)),
                max(1, int(hole.diameter / 2)),
                (0, 0, 255),
                1
            )

        return image