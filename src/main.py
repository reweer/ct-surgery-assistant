import cv2
import sys
import os
import argparse

sys.path.append(os.path.dirname(__file__))

from core.dicom_loader import load_dicom_series
from core.ct_model import CTModel
from core.controller import Controller
from interface.viewer import Viewer

def main():
    # Obsługa argumentów linii komend
    parser = argparse.ArgumentParser(description="CT Surgery Assistant - Przeglądarka skanów DICOM")
    parser.add_argument(
        "--study", "-s", 
        type=int, 
        choices=[1, 2, 3],
        default=1,
        help="Numer badania do wczytania (1, 2 lub 3). Domyślnie: 1"
    )
    args = parser.parse_args()

    # Konstruowanie ścieżki do danych
    # base_path to folder 'src'
    base_path = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(base_path)
    study_folder = f"zatoki_{args.study}"
    data_path = os.path.join(project_root, "data", study_folder, "DICOM")

    print(f"Wczytywanie badania nr {args.study} z: {data_path}")

    # Wczytywanie danych
    if not os.path.exists(data_path):
        print(f"Błąd: Ścieżka '{data_path}' nie istnieje. Upewnij się, że dane są w katalogu data.")
        sys.exit(1)

    volume = load_dicom_series(data_path)
    print("Volume shape:", volume.shape)

    model = CTModel(volume)
    viewer = Viewer()
    controller = Controller(model, viewer)

    # Pierwszy obraz
    viewer.update(model.get_current_slice())

    while True:
        key = cv2.waitKey(0)

        if key == 27:  # ESC
            break

        controller.handle_key(key)

if __name__ == "__main__":
    main()