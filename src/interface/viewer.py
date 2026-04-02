from PySide6.QtWidgets import QLabel, QApplication
from PySide6.QtGui import QImage, QPixmap, QPainter, QFont, QColor
from PySide6.QtCore import Qt
from utils.image_utils import apply_window, rotate_image


class Viewer(QLabel):

    def __init__(self):
        super().__init__()

        self.window_center = 40
        self.window_width = 400
        self.rotation = 0

        self.setScaledContents(False)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("background-color: black;")
        self.setMinimumSize(200, 200)

        self.controller = None  # 🔥 podpinamy z main
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFocus()
        self.current_image = None

    def resizeEvent(self, event):
        super().resizeEvent(event)

        if self.current_image is not None:
            self._render_current_image()

    def set_image(self, image):
        self.current_image = image
        self._render_current_image()

    def _render_current_image(self):
        if self.current_image is None:
            return

        image = apply_window(
            self.current_image,
            self.window_center,
            self.window_width
        )

        if self.rotation != 0:
            image = rotate_image(image, self.rotation)

        h, w = image.shape

        q_image = QImage(
            image.data,
            w,
            h,
            w,
            QImage.Format_Grayscale8
        )

        pixmap = QPixmap.fromImage(q_image)

        widget_w = self.width()
        widget_h = self.height()

        scaled = pixmap.scaled(
            widget_w,
            widget_h,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        final_pixmap = QPixmap(widget_w, widget_h)
        final_pixmap.fill(Qt.black)

        painter = QPainter(final_pixmap)

        x = (widget_w - scaled.width()) // 2
        y = (widget_h - scaled.height()) // 2

        painter.drawPixmap(x, y, scaled)

        painter.setPen(QColor(0, 255, 0))
        painter.setFont(QFont("Helvetica", 20, QFont.Bold))


        if self.controller is not None:
            index = self.controller.model.get_current_index()
            total = self.controller.model.get_total_slices()
            text = f"Slice: {index + 1} / {total}"
            painter.drawText(20, 30, text)



        painter.end()

        self.setPixmap(final_pixmap)
    

    def set_bone_window(self):
        self.window_center = 300
        self.window_width = 1500

    def set_soft_window(self):
        self.window_center = 40
        self.window_width = 400

    #  keyboard 
    def keyPressEvent(self, event):

        if self.controller is None:
            return

        key = event.key()
        changed = False

        if key == Qt.Key_D:
            changed = self.controller.handle_key("d")

        elif key == Qt.Key_A:
            changed = self.controller.handle_key("a")

        elif key == Qt.Key_1:
            changed = self.controller.handle_key("1")

        elif key == Qt.Key_2:
            changed = self.controller.handle_key("2")

        elif key == Qt.Key_Escape:
            QApplication.quit()
            return

        if changed:
            self.controller.update_view()