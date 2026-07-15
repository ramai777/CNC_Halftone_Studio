import cv2
import numpy as np


class ImageEnhancer:
    def __init__(self):
        self.gamma = 1.0
        self.clahe_clip = 2.0
        self.blur = 0
        self.sharpen = False

    def enhance(self, gray):

        image = gray.copy()

        # CLAHE
        clahe = cv2.createCLAHE(
            clipLimit=self.clahe_clip,
            tileGridSize=(8, 8)
        )

        image = clahe.apply(image)

        # Gamma
        inv = 1.0 / self.gamma

        table = np.array([
            ((i / 255.0) ** inv) * 255
            for i in np.arange(256)
        ]).astype("uint8")

        image = cv2.LUT(image, table)

        # Blur
        if self.blur > 0:
            k = self.blur * 2 + 1
            image = cv2.GaussianBlur(image, (k, k), 0)

        # Sharpen
        if self.sharpen:

            kernel = np.array([
                [0, -1, 0],
                [-1, 5, -1],
                [0, -1, 0]
            ])

            image = cv2.filter2D(image, -1, kernel)

        return image