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
from dxf_export import DXFExporter


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("CNC Halftone Studio")
        self.resize(1400, 850)

        self.processor = ImageProcessor()
        self.generator = HalftoneGenerator()
        self.preview_renderer = PreviewRenderer()
        self.exporter = DXFExporter()

        self.filename = None
        self.holes = []

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

        self.btnExport = QPushButton("💾 Экспорт DXF")
        self.btnExport.clicked.connect(self.export_dxf)

        left.addWidget(self.btnExport)

        stats = QGroupBox("Статистика")

        statsLayout = QVBoxLayout()

        self.lblHoles = QLabel("Отверстий: 0")
        self.lblMin = QLabel("Мин Ø: -")
        self.lblMax = QLabel("Макс Ø: -")
        self.lblAvg = QLabel("Средний Ø: -")

        statsLayout.addWidget(self.lblHoles)
        statsLayout.addWidget(self.lblMin)
        statsLayout.addWidget(self.lblMax)
        statsLayout.addWidget(self.lblAvg)

        stats.setLayout(statsLayout)

        left.addWidget(stats)
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

        # Автоматическое обновление после изменения параметров
        self.minBox.valueChanged.connect(self.generate)
        self.maxBox.valueChanged.connect(self.generate)
        self.bridgeBox.valueChanged.connect(self.generate)
    # ======================================

    def load_image(self):

        print("Кнопка нажата")

        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Открыть изображение",
            "",
            "Images (*.jpg *.jpeg *.png *.bmp)"
        )

        print(filename)
        

        if filename == "":
            return

        self.filename = filename
        print(filename)

        self.processor.load(filename)
        print("Изображение загружено")

        image = self.processor.get_gray()

        self.show_cv_image(image)

        self.generate()

    # ======================================

    def generate(self):

        if self.filename is None:
            return

        self.generator.min_diameter = self.minBox.value()
        self.generator.max_diameter = self.maxBox.value()
        self.generator.bridge = self.bridgeBox.value()

        holes = self.generator.generate(self.processor)

        self.holes = holes

        image = self.preview_renderer.render(
            self.processor,
            holes
        )

        self.show_cv_image(image)

        diameters = [h.diameter for h in holes]

        self.lblHoles.setText(
            f"Отверстий: {len(holes)}"
        )

        self.lblMin.setText(
            f"Мин Ø: {min(diameters):.2f} мм"
        )

        self.lblMax.setText(
            f"Макс Ø: {max(diameters):.2f} мм"
        )

        self.lblAvg.setText(
            f"Средний Ø: {sum(diameters)/len(diameters):.2f} мм"
        )
        # ======================================

    def export_dxf(self):

        if len(self.holes) == 0:
            return

        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить DXF",
            "portrait.dxf",
            "DXF (*.dxf)"
        )

        if filename == "":
            return

        self.exporter.export(
            filename,
            self.holes
        )

        print(f"DXF сохранен: {filename}")

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