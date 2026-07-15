from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QFileDialog
from PySide6.QtCore import Qt


def load_image(window):
    filename, _ = QFileDialog.getOpenFileName(
        window,
        "Выберите фотографию",
        "",
        "Изображения (*.jpg *.jpeg *.png *.bmp)"
    )

    if filename:
        pixmap = QPixmap(filename)

        pixmap = pixmap.scaled(
            window.preview.width(),
            window.preview.height(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        window.preview.setPixmap(pixmap)

        return filename

    return None