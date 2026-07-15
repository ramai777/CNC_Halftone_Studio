import sys
import cv2

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QPushButton,
    QLabel,
    QFileDialog,
    QHBoxLayout,
    QVBoxLayout,
    QGroupBox,
    QFormLayout,
    QDoubleSpinBox,
)

from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt

from image_processor import ImageProcessor
from halftone import HalftoneGenerator
from preview import PreviewRenderer


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("CNC Halftone Studio")
        self.resize(1400, 850)

        self.processor = ImageProcessor()
        self.generator = HalftoneGenerator()
        self.preview_renderer = PreviewRenderer()

        self.filename = None

        central = QWidget()
        self.setCentralWidget(central)

        layout = QHBoxLayout(central)

        # ------------------------
        # Левая панель
        # ------------------------

        left = QVBoxLayout()

        self.btnLoad = QPushButton("📷 Загрузить фотографию")
        self.btnLoad.clicked.connect(self.load_image)

        left.addWidget(self.btnLoad)

        settings = QGroupBox("Параметры")

        form = QFormLayout()

        self.widthBox = QDoubleSpinBox()
        self.widthBox.setValue(450)

        self.heightBox = QDoubleSpinBox()
        self.heightBox.setValue(600)

        self.minBox = QDoubleSpinBox()
        self.minBox.setValue(1)

        self.maxBox = QDoubleSpinBox()
        self.maxBox.setValue(4)

        self.bridgeBox = QDoubleSpinBox()
        self.bridgeBox.setValue(2.5)

        form.addRow("Ширина", self.widthBox)
        form.addRow("Высота", self.heightBox)
        form.addRow("Мин Ø", self.minBox)
        form.addRow("Макс Ø", self.maxBox)
        form.addRow("Перемычка", self.bridgeBox)

        settings.setLayout(form)

        left.addWidget(settings)

        self.btnGenerate = QPushButton("⚙ Генерировать")

        self.btnGenerate.clicked.connect(self.generate)

        left.addWidget(self.btnGenerate)

        left.addStretch()

        layout.addLayout(left, 1)

        # ------------------------
        # Правая часть
        # ------------------------

        self.preview = QLabel()

        self.preview.setAlignment(Qt.AlignCenter)

        self.preview.setStyleSheet("""
            background:white;
            border:1px solid gray;
        """)

        layout.addWidget(self.preview, 4)

    # ======================================

    def load_image(self):

        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Открыть изображение",
            "",
            "Images (*.jpg *.jpeg *.png *.bmp)"
        )

        if filename == "":
            return

        self.filename = filename

        self.processor.load(filename)

        image = self.processor.get_gray()

        self.show_cv_image(image)

    # ======================================

    def generate(self):

        if self.filename is None:
            return

        self.generator.min_diameter = self.minBox.value()
        self.generator.max_diameter = self.maxBox.value()
        self.generator.bridge = self.bridgeBox.value()

        holes = self.generator.generate(self.processor)

        image = self.preview_renderer.render(
            self.processor,
            holes
        )

        self.show_cv_image(image)

        print("Отверстий:", len(holes))

    # ======================================

    def show_cv_image(self, image):

        if len(image.shape) == 2:

            rgb = cv2.cvtColor(
                image,
                cv2.COLOR_GRAY2RGB
            )

        else:

            rgb = cv2.cvtColor(
                image,
                cv2.COLOR_BGR2RGB
            )

        h, w, ch = rgb.shape

        bytes_per_line = ch * w

        qt_image = QImage(
            rgb.data,
            w,
            h,
            bytes_per_line,
            QImage.Format_RGB888
        )

        pixmap = QPixmap.fromImage(qt_image)

        pixmap = pixmap.scaled(
            self.preview.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        self.preview.setPixmap(pixmap)


app = QApplication(sys.argv)

window = MainWindow()

window.show()

sys.exit(app.exec())