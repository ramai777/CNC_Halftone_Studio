import cv2
import numpy as np


class BrightnessSampler:

    def __init__(self, gray_image):
        self.image = gray_image

    def sample(self, x, y, radius=3):
        """
        Возвращает среднюю яркость вокруг точки.
        """

        h, w = self.image.shape

        x = int(round(x))
        y = int(round(y))

        x1 = max(0, x - radius)
        x2 = min(w - 1, x + radius)

        y1 = max(0, y - radius)
        y2 = min(h - 1, y + radius)

        roi = self.image[y1:y2 + 1, x1:x2 + 1]

        if roi.size == 0:
            return 255

        return float(np.mean(roi))