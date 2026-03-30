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

    # 🔹 load danych
    volume = load_dicom_series(data_path)
    print("Volume shape:", volume.shape)

    # 🔹 inicjalizacja
    model = CTModel(volume)
    viewer = Viewer()
    controller = Controller(model, viewer)
    voice = VoiceController()

    # 🔹 pierwszy obraz
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

        # 🔹 update
        viewer.update(model.get_current_slice())


if __name__ == "__main__":
    main()