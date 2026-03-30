## Sterowanie

| Klawisz | Funkcja |
|--------|--------|
| **a** | poprzedni slice |
| **d** | następny slice |
| **1** | tryb **bone** (kości) |
| **2** | tryb **soft tissue** (tkanki miękkie) |
| **ESC** | wyjście |

---

## Setup (pierwsze uruchomienie)

### 1. Sklonuj repozytorium

```bash
git clone https://github.com/reweer/ct-surgery-assistant.git
cd ct-surgery-assistant
```

### 2. Stwórz środowisko wirtualne
```
python3 -m venv venv
source venv/bin/activate
```

### 3. Zainstaluj zależności
```
pip install -r requirements.txt
```

##  Dane 
Każdy musi dodać własne dane do folderu: data/ct/

W pliku main.py ustaw ścieżkę do danych:
```
DATA_PATH = "data/ct/Badania/Zatoki 1/DICOM"
```
## Model VOSK
Sterowanie głosowe wykorzystuje bibliotekę **VOSK**.

Model nie jest dołączony do repozytorium (duży rozmiar), więc każdy musi pobrać go lokalnie.

### Pobranie modelu
1. Wejdź na:
https://alphacephei.com/vosk/models

2. Pobierz model:
```
vosk-model-small-en-us-0.15
```

Następnie uruchom:
```
python3 src/main.py
```
## Struktura projektu
```
src/
├── core/         # wczytywanie DICOM i model danych
├── interface/    # viewer (OpenCV)
├── interaction/  # input (voice – do zrobienia)
└── utils/        # przetwarzanie obrazu
```
