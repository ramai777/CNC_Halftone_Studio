import cv2

from image_enhancer import ImageEnhancer


class ImageProcessor:

    def __init__(self):
        self.image = None
        self.gray = None

        self.enhancer = ImageEnhancer()

    def load(self, filename):

        self.image = cv2.imread(filename)

        if self.image is None:
            raise Exception("Не удалось открыть изображение")

        gray = cv2.cvtColor(
            self.image,
            cv2.COLOR_BGR2GRAY
        )

        # Вся обработка изображения теперь здесь
        self.gray = self.enhancer.enhance(gray)

    def width(self):
        return self.gray.shape[1]

    def height(self):
        return self.gray.shape[0]

    def brightness(self, x, y):

        x = max(0, min(x, self.width() - 1))
        y = max(0, min(y, self.height() - 1))

        return int(self.gray[y, x])

    def get_gray(self):
        return self.gray