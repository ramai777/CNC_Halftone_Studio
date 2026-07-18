import cv2
import numpy as np


class PreviewRenderer:

    def render(
        self,
        processor,
        holes,
        show_background=False
    ):

        if show_background:

            image = cv2.cvtColor(
                processor.get_gray(),
                cv2.COLOR_GRAY2BGR
            )

        else:

            image = np.full(
                (
                    processor.height(),
                    processor.width(),
                    3
                ),
                255,
                dtype=np.uint8
            )

        for hole in holes:

            radius = max(
                1,
                int(hole.diameter / 2)
            )

            color = (0, 0, 0)

            cv2.circle(
                image,
                (
                    int(hole.x),
                    int(hole.y)
                ),
                radius,
                color,
                -1
            )

        return image