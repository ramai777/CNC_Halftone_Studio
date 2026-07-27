from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt, Signal


class PreviewWidget(QLabel):

    imageMoved = Signal(float, float)
    imageScaled = Signal(float)

    def __init__(self):
        super().__init__()

        self.setMouseTracking(True)

        self.dragging = False
        self.lastPos = None

    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.lastPos = event.position()

    def mouseMoveEvent(self, event):

        if not self.dragging:
            return

        pos = event.position()

        dx = pos.x() - self.lastPos.x()
        dy = pos.y() - self.lastPos.y()

        self.lastPos = pos

        self.imageMoved.emit(dx, dy)

    def mouseReleaseEvent(self, event):

        self.dragging = False

    def wheelEvent(self, event):

        delta = event.angleDelta().y()

        if delta > 0:
            self.imageScaled.emit(1.05)
        else:
            self.imageScaled.emit(0.95)