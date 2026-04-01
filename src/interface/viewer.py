from PySide6.QtWidgets import QLabel, QApplication
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import Qt
import numpy as np
import cv2
from PySide6.QtGui import QPainter, QFont, QColor
from utils.image_utils import apply_window
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class Viewer(QLabel):

    def __init__(self):
        super().__init__()

        self.window_center = 40
        self.window_width = 400

        self.setMinimumSize(800, 800)
        self.setScaledContents(False)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("background-color: black;")

        self.controller = None  # 🔥 podpinamy z main
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFocus()



    def set_image(self, image):

        image = apply_window(
            image,
            self.window_center,
            self.window_width
        )

        h, w = image.shape

        q_image = QImage(
            image.data,
            w,
            h,
            w,
            QImage.Format_Grayscale8
        )

        pixmap = QPixmap.fromImage(q_image)
        pixmap = pixmap.scaled(
            self.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )


        self.setPixmap(pixmap)


    def set_image(self, image):

        image = apply_window(
            image,
            self.window_center,
            self.window_width
        )

        h, w = image.shape

        # konwersja do QImage
        q_image = QImage(
            image.data,
            w,
            h,
            w,
            QImage.Format_Grayscale8
        )

        pixmap = QPixmap.fromImage(q_image)

        # rozmiar widgetu
        widget_w = self.width()
        widget_h = self.height()

        # skalowanie z zachowaniem proporcji
        scaled = pixmap.scaled(
            widget_w,
            widget_h,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        # 🔥 czarne tło (canvas)
        final_pixmap = QPixmap(widget_w, widget_h)
        final_pixmap.fill(Qt.black)

        # wklejenie obrazu na środek
        painter = QPainter(final_pixmap)

        x = (widget_w - scaled.width()) // 2
        y = (widget_h - scaled.height()) // 2

        painter.drawPixmap(x, y, scaled)

    # TEKST W CZARNYM OBSZARZE
        painter.setPen(QColor(0, 255, 0))
        painter.setFont(QFont("Inter", 20, QFont.Bold))

        index = self.controller.model.index
        total = len(self.controller.model.volume)

        text = f"Slice: {index+1} / {total}"

        painter.drawText(20, 30, text)  # ← zawsze w górnym czarnym obszarze

        painter.end()

        self.setPixmap(final_pixmap)
    

    def set_bone_window(self):
        self.window_center = 300
        self.window_width = 1500

    def set_soft_window(self):
        self.window_center = 40
        self.window_width = 400

    # 🔥 keyboard (POPRAWNIE)
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