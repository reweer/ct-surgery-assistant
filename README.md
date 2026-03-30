# CT Surgery Assistant

Proste narzędzie do przeglądania skanów tomografii komputerowej (CT) w formacie DICOM.

## Setup (pierwsze uruchomienie)

### 1. Sklonuj repozytorium
```bash
git clone https://github.com/reweer/ct-surgery-assistant.git
cd ct-surgery-assistant
```

### 2. Stwórz środowisko wirtualne
Zaleca się użycie środowiska wirtualnego, szczególnie na systemach macOS i Linux:
```bash
python3 -m venv venv
```

### 3. Aktywuj środowisko i zainstaluj biblioteki
```bash
source venv/bin/activate
pip install -r requirements.txt
```

## Konfiguracja danych
1. Folder `data` znajduje się w głównym katalogu projektu (`ct-surgery-assistant/data`).
2. Dane są zorganizowane w podfolderach:
   - `data/zatoki_1/DICOM`
   - `data/zatoki_2/DICOM`
   - `data/zatoki_3/DICOM`
*Uwaga: Pliki DICOM są ignorowane przez Git i nie zostaną wysłane do repozytorium.*

## Uruchamianie
*Pamiętaj, aby przed uruchomieniem zawsze aktywować środowisko komendą `source venv/bin/activate`.*

Aby uruchomić aplikację z domyślnym badaniem (nr 1):
```bash
python3 src/main.py
```

### Wybór konkretnego badania
Możesz wybrać badanie (1, 2 lub 3) używając flagi `--study` lub `-s`:
```bash
python3 src/main.py --study 2
```

## Sterowanie (w aktywnym oknie "CT Viewer")

| Klawisz | Funkcja |
|--------|--------|
| **a** | poprzedni slice |
| **d** | następny slice |
| **1** | tryb **bone** (kości) |
| **2** | tryb **soft tissue** (tkanki miękkie) |
| **ESC** | wyjście |

## Sterowanie głosowe (Model VOSK)
Projekt wspiera sterowanie głosowe przy użyciu biblioteki **VOSK**.

Model nie jest dołączony do repozytorium ze względu na rozmiar. Każdy użytkownik musi pobrać go lokalnie:

1. Wejdź na stronę: [https://alphacephei.com/vosk/models](https://alphacephei.com/vosk/models)
2. Pobierz model: `vosk-model-small-en-us-0.15`
3. Rozpakuj go w głównym katalogu projektu.

## Struktura projektu
```
src/
├── core/         # wczytywanie DICOM i model danych
├── interface/    # viewer (OpenCV)
├── interaction/  # input (voice)
└── utils/        # przetwarzanie obrazu
```
