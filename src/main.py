import cv2
import sys
import os
import argparse

sys.path.append(os.path.dirname(__file__))

from core.dicom_loader import load_dicom_series
from core.ct_model import CTModel
from core.controller import Controller
from interface.viewer import Viewer
from interaction.voice import VoiceController


def main():
    # 🔹 argumenty (wybór badania)
    parser = argparse.ArgumentParser(description="CT Surgery Assistant")
    parser.add_argument(
        "--study", "-s",
        type=int,
        choices=[1, 2, 3],
        default=1,
        help="Numer badania (1, 2, 3)"
    )
    args = parser.parse_args()

    # 🔹 ścieżka do danych
    base_path = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(base_path)
    study_folder = f"zatoki_{args.study}"
    data_path = os.path.join(project_root, "data", study_folder, "DICOM")

    print(f"Loading study {args.study} from: {data_path}")

    if not os.path.exists(data_path):
        print("❌ Data path does not exist")
        sys.exit(1)

    # load danych
    volume = load_dicom_series(data_path)
    print("Volume shape:", volume.shape)

    # inicjalizacja
    model = CTModel(volume)
    viewer = Viewer()
    controller = Controller(model, viewer)
    voice = VoiceController()

    #pierwszy obraz
    #viewer.update(model.get_current_slice())

    needs_update = True

    while True:

        key = cv2.waitKey(1)

        if key == 27:
            break

        if key != -1:
            if controller.handle_key(key):
                needs_update = True

        command = voice.last_command

        if command:
            voice.last_command = None

            if controller.handle_voice(command):
                needs_update = True
        #render tylko gdy cos sie zmienilo
        if needs_update:
            controller.update_view()
            needs_update = False





if __name__ == "__main__":
    main()