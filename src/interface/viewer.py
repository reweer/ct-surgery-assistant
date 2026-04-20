from PySide6.QtWidgets import QLabel, QApplication, QPushButton
from PySide6.QtGui import QImage, QPixmap, QPainter, QFont, QColor, QBrush
from PySide6.QtCore import Qt
from utils.image_utils import apply_window, rotate_image


class Viewer(QLabel):

    def __init__(self):
        super().__init__()

        self.window_center = 40
        self.window_width = 400
        self.rotation = 0
        
        self.DEFAULT_CENTER = 40
        self.DEFAULT_WIDTH = 400

        self.window_center = self.DEFAULT_CENTER
        self.window_width = self.DEFAULT_WIDTH

        self.setScaledContents(False)
        self.setAlignment(Qt.AlignCenter)
        self._uniform_bg = QColor(18, 18, 22)
        self._apply_background_style()
        self.setMinimumSize(200, 200)

        self.controller = None
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFocus()
        self.current_image = None

        self.ar_transparent = False
        self._top_bar_h = 52

        self._ar_btn = QPushButton("AR: wyl.", self)
        self._ar_btn.setToolTip("Wlacza przezroczyste tlo okna (nakladka AR / gogle)")
        self._ar_btn.setFocusPolicy(Qt.NoFocus)
        self._ar_btn.setFixedHeight(28)
        self._ar_btn.clicked.connect(self._toggle_ar_mode)

    def _apply_background_style(self):
        c = self._uniform_bg
        self.setStyleSheet(
            f"background-color: rgb({c.red()}, {c.green()}, {c.blue()});"
        )

    def _toggle_ar_mode(self):
        self.ar_transparent = not self.ar_transparent
        self._ar_btn.setText("AR: wl." if self.ar_transparent else "AR: wyl.")
        win = self.window()
        if win is not None:
            win.setAttribute(Qt.WA_TranslucentBackground, self.ar_transparent)
            if self.ar_transparent:
                win.setStyleSheet("QMainWindow { background: transparent; }")
            else:
                win.setStyleSheet("")
        self.setAttribute(Qt.WA_TranslucentBackground, self.ar_transparent)
        if self.ar_transparent:
            self.setStyleSheet("background-color: transparent;")
        else:
            self._apply_background_style()
        if self.current_image is not None:
            self._render_current_image()

    def _layout_ar_button(self):
        margin = 8
        self._ar_btn.adjustSize()
        y = max(0, (self._top_bar_h - self._ar_btn.height()) // 2)
        self._ar_btn.move(
            max(0, self.width() - self._ar_btn.width() - margin),
            y,
        )
        self._ar_btn.raise_()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._layout_ar_button()

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
        self._layout_ar_button()

        bar_h = self._top_bar_h
        content_w = widget_w
        content_h = max(1, widget_h - bar_h)

        scaled = pixmap.scaled(
            int(content_w * self.controller.zoom),
            int(content_h * self.controller.zoom),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        if self.controller is not None:
            scaled_w = scaled.width()
            scaled_h = scaled.height()
            self.controller.clamp(
                scaled_w,
                scaled_h,
                content_w,
                content_h
            )

        final_pixmap = QPixmap(widget_w, widget_h)
        if self.ar_transparent:
            final_pixmap.fill(Qt.transparent)
        else:
            final_pixmap.fill(self._uniform_bg)

        painter = QPainter(final_pixmap)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

        x = (content_w - scaled.width()) // 2 + int(self.controller.offset_x)
        y = bar_h + (content_h - scaled.height()) // 2 + int(self.controller.offset_y)

        painter.drawPixmap(x, y, scaled)

        if self.controller is not None:
            self._draw_status_overlay(painter, widget_w, widget_h)

        painter.end()

        self.setPixmap(final_pixmap)

    def _draw_status_overlay(self, painter, widget_w, widget_h):
        index = self.controller.model.get_current_index()
        total = self.controller.model.get_total_slices()
        zoom_pct = int(round(self.controller.zoom * 100))
        last = (self.controller.last_voice_transcript or "").strip()
        if not last:
            last = "-"
        if len(last) > 80:
            last = last[:77] + "..."

        bar_h = self._top_bar_h
        margin_x = 10
        btn_reserve = self._ar_btn.width() + 20

        painter.setPen(Qt.NoPen)
        bg = QColor(0, 0, 0, 185) if not self.ar_transparent else QColor(0, 0, 0, 215)
        painter.setBrush(QBrush(bg))
        painter.drawRect(0, 0, widget_w, bar_h)

        font = QFont("Segoe UI", 20, QFont.Bold)
        painter.setFont(font)
        fm = painter.fontMetrics()
        line = (
            f"Slice: {index + 1} / {total}     "
            f"Zoom: {zoom_pct}%     "
            f"Ostatnia komenda: {last}"
        )
        text_max = max(80, widget_w - btn_reserve - margin_x)
        elided = fm.elidedText(line, Qt.ElideRight, text_max)

        painter.setPen(QColor(0, 255, 0))
        painter.drawText(
            margin_x,
            0,
            text_max,
            bar_h,
            Qt.AlignLeft | Qt.AlignVCenter,
            elided,
        )


    #def set_bone_window(self):
     #   self.window_center = 300
      #  self.window_width = 1500

   # def set_soft_window(self):
    #    self.window_center = 40
     #   self.window_width = 400
    # --- POPRAWIONE PRESETY MEDYCZNE ---
    
    def set_bone_window(self):
        self.window_center = 600
        self.window_width = 2000
        # Jeśli masz suwaki, zaktualizuj ich pozycję tutaj:
        if hasattr(self, 'bright_slider'):
            self.bright_slider.setValue(600)
            self.contrast_slider.setValue(2000)
        self._render_current_image()

    def set_soft_window(self):
        self.window_center = 40
        self.window_width = 400
        # Jeśli masz suwaki, zaktualizuj ich pozycję tutaj:
        if hasattr(self, 'bright_slider'):
            self.bright_slider.setValue(40)
            self.contrast_slider.setValue(400)
        self._render_current_image()
    def set_sinus_window(self):
        """Optymalne okno do operacji zatok (Sinus Window)."""
        self.window_center = 300
        self.window_width = 2500
        self._render_current_image()

    def change_window(self, center_delta=0, width_delta=0):
        """
        Zmienia parametry okna o konkretną wartość i odświeża obraz.
        Wywoływana przez Controller przy komendach głosowych.
        """
        self.window_center += center_delta
        self.window_width += width_delta
        
        # Zabezpieczenie przed ujemną szerokością okna
        if self.window_width < 1:
            self.window_width = 1
            
        print(f"[VIEWER] Window updated: Center={self.window_center}, Width={self.window_width}")
        self._render_current_image()
        
    def reset_window(self):
        """
        Przywraca domyślne ustawienia brightness/contrast
        i odświeża obraz.
        """
        self.window_center = self.DEFAULT_CENTER
        self.window_width = self.DEFAULT_WIDTH

        if hasattr(self, 'bright_slider'):
            self.bright_slider.setValue(self.DEFAULT_CENTER)
            self.contrast_slider.setValue(self.DEFAULT_WIDTH)

        print(f"[VIEWER] Window reset: Center={self.window_center}, Width={self.window_width}")
        self._render_current_image()    
    
    
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
        elif key == Qt.Key_3:
            changed = self.controller.handle_key("3")
        elif key == Qt.Key_R:
            changed = self.controller.handle_key("r")
            
        

        elif key == Qt.Key_Escape:
            QApplication.quit()
            return
        elif key == Qt.Key_Plus:
            changed = self.controller.execute_action("zoom_in")

        elif key == Qt.Key_Minus:
            changed = self.controller.execute_action("zoom_out")

        elif key == Qt.Key_Left:
            changed = self.controller.execute_action("left")

        elif key == Qt.Key_Right:
            changed = self.controller.execute_action("right")

        elif key == Qt.Key_Up:
            changed = self.controller.execute_action("up")

        elif key == Qt.Key_Down:
            changed = self.controller.execute_action("down")

        elif key == Qt.Key_C:
            changed = self.controller.execute_action("center")

        if changed:
            self.controller.update_view()