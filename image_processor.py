import cv2
import numpy as np

from image_transform import ImageTransform

class ImageProcessor:
    

    def __init__(self):
        self.image = None

        self.original_gray = None
        self.gray = None

        self.transform = ImageTransform()

    def load(self, filename):

        import numpy as np

        data = np.fromfile(filename, dtype=np.uint8)

        self.image = cv2.imdecode(data, cv2.IMREAD_COLOR)

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

        self.original_gray = gray
        self.gray = gray.copy()

    def resize_to_panel(
        self,
        width_mm,
        height_mm,
        pixels_per_mm
    ):
        """
        Масштабирует изображение под размер изделия.
        """

        target_w = int(width_mm * pixels_per_mm)
        target_h = int(height_mm * pixels_per_mm)

        self.gray = cv2.resize(
            self.original_gray,
            (target_w, target_h),
            interpolation=cv2.INTER_AREA
        )
        print("Размер после resize:", self.gray.shape)
        print("pixels_per_mm =", pixels_per_mm)
        
    def transform_image(
        self,
        width_px,
        height_px
    ):
        self.gray = self.transform.apply(
            self.gray,
            width_px,
            height_px
        )


    def width(self):
        return self.gray.shape[1]

    def height(self):
        return self.gray.shape[0]

    def brightness(self, x, y):
        return int(self.gray[y, x])

    def get_gray(self):
        return self.gray