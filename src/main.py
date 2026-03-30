import cv2
import os
import sys

sys.path.append(os.path.dirname(__file__))

from core.dicom_loader import load_dicom_series
from core.ct_model import CTModel
from core.controller import Controller
from interface.viewer import Viewer
from interaction.voice import VoiceController

# 👉 ścieżka do danych
DATA_PATH = "/Users/oliwiarewer/Downloads/ct-surgery-assistant/data/ct/Badania/ZAtoki 1/DICOM"

# load danych
volume = load_dicom_series(DATA_PATH)
print("Volume shape:", volume.shape)

# inicjalizacja
model = CTModel(volume)
viewer = Viewer()
controller = Controller(model, viewer)
voice = VoiceController()

# startowy obraz
viewer.update(model.get_current_slice())

while True:

    # 🔹 klawiatura (non-blocking)
    key = cv2.waitKey(1)

    if key == 27:  # ESC
        break

    if key != -1:
        controller.handle_key(key)

    # 🔹 voice
    command = voice.listen()

    if "next" in command:
        model.next_slice()

    elif "previous" in command:
        model.previous_slice()

    elif "bone" in command:
        viewer.set_bone_window()

    elif "soft" in command:
        viewer.set_soft_window()

    # update view
    viewer.update(model.get_current_slice())