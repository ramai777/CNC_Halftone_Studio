import cv2
import numpy as np


class ImageProcessor:

    def __init__(self):
        self.image = None
        self.gray = None

    def load(self, filename):

        self.image = cv2.imread(filename)

        if self.image is None:
            raise Exception("Не удалось открыть изображение")

        gray = cv2.cvtColor(
            self.image,
            cv2.COLOR_BGR2GRAY
        )

        # Автоконтраст
        gray = cv2.equalizeHist(gray)

        # CLAHE - усиливает локальные детали
        clahe = cv2.createCLAHE(
            clipLimit=2.0,
            tileGridSize=(8, 8)
        )

        gray = clahe.apply(gray)

        # Небольшое размытие убирает шум
        gray = cv2.GaussianBlur(
            gray,
            (3, 3),
            0
        )

        self.gray = gray

    def width(self):
        return self.gray.shape[1]

    def height(self):
        return self.gray.shape[0]

    def brightness(self, x, y):
        return int(self.gray[y, x])

    def get_gray(self):
        return self.gray