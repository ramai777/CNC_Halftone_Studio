import cv2
import numpy as np


class BrightnessSampler:

    def __init__(self, gray_image):
        self.image = gray_image

    def sample(self, x, y, diameter):
        """
        Возвращает среднюю яркость внутри круглой области.
        Размер области зависит от диаметра будущего отверстия.
        """

        radius = max(2, int(round(diameter / 2)))

        h, w = self.image.shape

        x = int(round(x))
        y = int(round(y))

        x1 = max(0, x - radius)
        y1 = max(0, y - radius)

        x2 = min(w, x + radius + 1)
        y2 = min(h, y + radius + 1)

        roi = self.image[y1:y2, x1:x2]

        if roi.size == 0:
            return 255

        mask = np.zeros(roi.shape, dtype=np.uint8)

        cy = roi.shape[0] // 2
        cx = roi.shape[1] // 2

        cv2.circle(
            mask,
            (cx, cy),
            radius,
            255,
            -1
        )

        return cv2.mean(roi, mask=mask)[0]
    def contrast(self, x, y, radius=5):
        """
        Возвращает локальный контраст.
        """

        h, w = self.image.shape

        x = int(round(x))
        y = int(round(y))

        x1 = max(0, x - radius)
        y1 = max(0, y - radius)

        x2 = min(w, x + radius + 1)
        y2 = min(h, y + radius + 1)

        roi = self.image[y1:y2, x1:x2]

        if roi.size == 0:
            return 0

        return float(roi.std())