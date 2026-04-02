# CT Surgery Assistant

Proste narzędzie do przeglądania skanów tomografii komputerowej (CT) w formacie DICOM z obsługą sterowania głosowego.

## Setup (pierwsze uruchomienie)

### 1. Sklonuj repozytorium
```bash
git clone https://github.com/reweer/ct-surgery-assistant.git
cd ct-surgery-assistant
```

### 2. Stwórz środowisko wirtualne
```bash
python3 -m venv venv
```

### 3. Aktywuj środowisko i zainstaluj biblioteki
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Konfiguracja Mikrofonu (Ważne!)
Aby uniknąć problemów z niewłaściwym urządzeniem wejściowym (np. słuchawki vs wbudowany mikrofon), uruchom:
```bash
python3 setup_audio.py
```
Skrypt wyświetli listę dostępnych urządzeń i pozwoli Ci wybrać to, którego chcesz używać. Wybór zostanie zapisany lokalnie w pliku `config.json` (plik indywidyalny dla kazdego, tworzony przy pierwszym uruchomieniu `setup_audio.py` - ignorowany przez git).

## Sterowanie Głosowe (Model VOSK)
Projekt wymaga modelu VOSK. Możesz go pobrać i wypakować za pomocą poniższych komend:

```bash
mkdir -p models
curl -L https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip -o models/model.zip
unzip models/model.zip -d models/
```

Przykładowy wynik w terminalu:
```text
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 39.2M  100 39.2M    0     0  21.6M      0  0:00:01  0:00:01 --:--:-- 21.6M
Archive:  models/model.zip
```

## Uruchamianie
```bash
python3 src/main.py --study 1
```

## Sterowanie

### Klawiatura
| Klawisz | Funkcja |
|--------|--------|
| **a** | poprzedni slice |
| **d** | następny slice |
| **1** | tryb **bone** (kości) |
| **2** | tryb **soft tissue** (tkanki miękkie) |
| **ESC** | wyjście |

### Komendy Głosowe (Język Angielski)
Mów wyraźnie do mikrofonu po pojawieniu się komunikatu `🎤 Voice thread running...`.

| Komenda | Funkcja | Przykład |
|--------|--------|--------|
| **Next / Previous** | Przeskok o 1 slice | "next", "back" |
| **Next X / Back X** | Przeskok o X sliców | "next five", "back twenty" |
| **Slice X** | Skok do konkretnego numeru | "slice fifty", "slice 10" |
| **First / Last / Middle** | Skok do granic badania | "first slice", "middle slice" |
| **Bone / Soft** | Zmiana okna widoku | "bone window", "soft" |

*Obsługiwane liczby słownie: zero - hundred, thousand.*

## Testowanie
Skrypt testowy nawigacji:
```bash
python3 tests/test_navigation.py
```
Pełen scenariusz testowy znajduje się w pliku `TESTING_SCENARIO.md`.

## Struktura projektu
```
src/
├── core/         # wczytywanie DICOM, model danych i kontroler
├── interface/    # viewer (PySide6)
├── interaction/  # obsługa głosu (Vosk)
└── utils/        # przetwarzanie obrazu
```
