import sys
import os
import argparse
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import QTimer

sys.path.append(os.path.dirname(__file__))

from core.dicom_loader import load_dicom_series
from core.ct_model import CTModel
from core.controller import Controller
from interface.viewer import Viewer
from interaction.voice import VoiceController


def main():

    app = QApplication(sys.argv)

    # argumenty + path
    parser = argparse.ArgumentParser()
    parser.add_argument("--study", "-s", type=int, default=1)
    args = parser.parse_args()

    base_path = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(base_path)
    study_folder = f"zatoki_{args.study}"
    data_path = os.path.join(project_root, "data", study_folder, "DICOM")

    volume = load_dicom_series(data_path)

    model = CTModel(volume)
    viewer = Viewer()
    controller = Controller(model, viewer)
    voice = VoiceController()

    viewer.controller = controller

    # NOWY BLOK UI 
    window = QMainWindow()
    window.setCentralWidget(viewer)

    window.resize(1000, 800)
    window.show()

    viewer.setFocus()

    #  pierwszy render
    controller.update_view()
    

    #  TIMER (voice loop)
    def check_voice():

        changed = False

        while not voice.commands.empty():
            command = voice.commands.get()

            if controller.handle_voice(command):
                changed = True

        if changed:
            controller.update_view()

    timer = QTimer()
    timer.timeout.connect(check_voice)
    timer.start(50)

    sys.exit(app.exec())




if __name__ == "__main__":
    main()