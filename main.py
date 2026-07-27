import sys
import cv2

from preview_widget import PreviewWidget
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
from project import Project


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("CNC Halftone Studio")
        self.resize(1400, 850)

        self.project = Project()

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
        self.widthBox.setRange(10, 5000)
        self.widthBox.setValue(450)

        self.heightBox = QDoubleSpinBox()
        self.heightBox.setRange(10, 5000)
        self.heightBox.setValue(600)

        self.minBox = QDoubleSpinBox()
        self.minBox.setValue(1)

        self.maxBox = QDoubleSpinBox()
        self.maxBox.setValue(4)

        self.bridgeBox = QDoubleSpinBox()
        self.bridgeBox.setValue(2.5)

        self.gridStepBox = QDoubleSpinBox()
        self.gridStepBox.setRange(2.0, 10.0)
        self.gridStepBox.setSingleStep(0.1)
        self.gridStepBox.setValue(5.0)

        self.gammaBox = QDoubleSpinBox()
        self.gammaBox.setDecimals(2)
        self.gammaBox.setRange(0.2, 5.0)
        self.gammaBox.setSingleStep(0.1)
        self.gammaBox.setValue(1.8)

        self.scaleBox = QDoubleSpinBox()
        self.scaleBox.setRange(0.2, 3.0)
        self.scaleBox.setSingleStep(0.05)
        self.scaleBox.setValue(1.0)

        self.offsetXBox = QDoubleSpinBox()
        self.offsetXBox.setRange(-500, 500)
        self.offsetXBox.setValue(0)

        self.offsetYBox = QDoubleSpinBox()
        self.offsetYBox.setRange(-500, 500)
        self.offsetYBox.setValue(0)

        form.addRow("Ширина", self.widthBox)
        form.addRow("Высота", self.heightBox)
        form.addRow("Мин Ø", self.minBox)
        form.addRow("Макс Ø", self.maxBox)
        form.addRow("Перемычка", self.bridgeBox)
        form.addRow("Шаг сетки", self.gridStepBox)
        form.addRow("Gamma", self.gammaBox)
        form.addRow("Масштаб", self.scaleBox)
        form.addRow("Смещение X", self.offsetXBox)
        form.addRow("Смещение Y", self.offsetYBox)

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

        previewLayout = QHBoxLayout()

        self.originalPreview = PreviewWidget()
        self.originalPreview.setAlignment(Qt.AlignCenter)
        self.originalPreview.setStyleSheet("""
        background:white;
        border:1px solid gray;
        """)

        self.preview = PreviewWidget()
        self.preview.setAlignment(Qt.AlignCenter)
        self.preview.setStyleSheet("""
        background:white;
        border:1px solid gray;
        """)

        previewLayout.addWidget(self.originalPreview)
        previewLayout.addWidget(self.preview)

        layout.addLayout(previewLayout, 4)

        # Автоматическое обновление после изменения параметров
        self.minBox.valueChanged.connect(self.generate)
        self.maxBox.valueChanged.connect(self.generate)
        self.bridgeBox.valueChanged.connect(self.generate)
        self.gridStepBox.valueChanged.connect(self.generate)
        self.gammaBox.valueChanged.connect(self.generate)
        self.scaleBox.valueChanged.connect(self.generate)
        self.offsetXBox.valueChanged.connect(self.generate)
        self.offsetYBox.valueChanged.connect(self.generate)
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

        self.show_cv_image(
            image,
            self.originalPreview
        )

        self.generate()

    # ======================================

    def generate(
        self,
        pixels_per_mm=None
    ):
        print(">>> GENERATE START <<<")

        if pixels_per_mm is None:
            pixels_per_mm = self.generator.settings.preview_pixels_per_mm

        if self.filename is None:
            return
        
        self.processor.resize_to_panel(
            self.widthBox.value(),
            self.heightBox.value(),
            pixels_per_mm
        )
        print("После resize:", self.processor.get_gray().shape)

        pixels_per_mm = self.generator.settings.preview_pixels_per_mm

        self.processor.transform.scale = self.scaleBox.value()

        self.processor.transform.offset_x = (
            self.offsetXBox.value() * pixels_per_mm
        )

        self.processor.transform.offset_y = (
            self.offsetYBox.value() * pixels_per_mm
        )

        self.processor.transform_image(
            int(self.widthBox.value() * pixels_per_mm),
            int(self.heightBox.value() * pixels_per_mm)
        )
        print("После transform:", self.processor.get_gray().shape)

        self.generator.settings.panel_width_mm = self.widthBox.value()
        self.generator.settings.panel_height_mm = self.heightBox.value()

        self.generator.settings.min_diameter = self.minBox.value()
        self.generator.settings.max_diameter = self.maxBox.value()
        self.generator.settings.bridge = self.bridgeBox.value()
        self.generator.settings.grid_step = self.gridStepBox.value()

        self.generator.settings.gamma = self.gammaBox.value()
        self.generator.settings.image_scale = self.scaleBox.value()
        self.generator.settings.offset_x_mm = self.offsetXBox.value()
        self.generator.settings.offset_y_mm = self.offsetYBox.value()

        
        holes = self.generator.generate(self.processor)

        print("Генерация закончилась")

        self.holes = holes

        print("Перед PreviewRenderer")

        image = self.preview_renderer.render(
            self.processor,
            holes
        )

        print("После PreviewRenderer")

        self.show_cv_image(
            image,
            self.preview
        )

        print("После show_cv_image")

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
    def generate_preview(self):
        self.generate(
            pixels_per_mm=self.generator.settings.preview_pixels_per_mm
        )

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

    def show_cv_image(
        self,
        image,
        label
    ):

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

        label.setPixmap(pixmap)


app = QApplication(sys.argv)

window = MainWindow()

window.show()

sys.exit(app.exec())