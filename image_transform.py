import cv2
import numpy as np


class ImageTransform:

    def __init__(self):
        self.scale = 1.0
        self.offset_x = 0
        self.offset_y = 0

    def apply(
        self,
        image,
        target_width,
        target_height
    ):
        """
        Масштабирует изображение с сохранением пропорций,
        автоматически центрирует его и позволяет двигать.
        """

        h, w = image.shape[:2]

        # Автоматический масштаб "Вписать"
        fit_scale = min(
            target_width / w,
            target_height / h
        )

        final_scale = fit_scale * self.scale

        new_w = max(1, int(w * final_scale))
        new_h = max(1, int(h * final_scale))

        resized = cv2.resize(
            image,
            (new_w, new_h),
            interpolation=cv2.INTER_AREA
        )

        # Белый холст нужного размера
        canvas = np.full(
            (target_height, target_width),
            255,
            dtype=np.uint8
        )

        # Центрируем
        x = (target_width - new_w) // 2 + int(self.offset_x)
        y = (target_height - new_h) // 2 + int(self.offset_y)

        # Координаты назначения
        dst_x1 = max(0, x)
        dst_y1 = max(0, y)

        dst_x2 = min(target_width, x + new_w)
        dst_y2 = min(target_height, y + new_h)

        # Координаты источника
        src_x1 = max(0, -x)
        src_y1 = max(0, -y)

        src_x2 = src_x1 + (dst_x2 - dst_x1)
        src_y2 = src_y1 + (dst_y2 - dst_y1)

        if dst_x2 > dst_x1 and dst_y2 > dst_y1:

            canvas[
                dst_y1:dst_y2,
                dst_x1:dst_x2
            ] = resized[
                src_y1:src_y2,
                src_x1:src_x2
            ]

        return canvas