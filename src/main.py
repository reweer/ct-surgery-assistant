import sys
import os
sys.path.append(os.path.dirname(__file__))


import cv2
import sys
import os

sys.path.append(os.path.dirname(__file__))

from core.dicom_loader import load_dicom_series
from core.ct_model import CTModel
from core.controller import Controller
from interface.viewer import Viewer

#TU ustaw ścieżkę do danych
volume = load_dicom_series("/Users/oliwiarewer/Downloads/ct-surgery-assistant/data/ct/Badania/ZAtoki 1/DICOM")

print("Volume shape:", volume.shape)

model = CTModel(volume)
viewer = Viewer()
controller = Controller(model, viewer)

# pierwszy obraz
viewer.update(model.get_current_slice())

while True:

    key = cv2.waitKey(0)

    if key == 27:  # ESC
        break

    controller.handle_key(key)