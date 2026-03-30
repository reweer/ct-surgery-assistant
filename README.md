# CT Surgery Assistant

Proste narzędzie do przeglądania skanów tomografii komputerowej (CT) w formacie DICOM.

## Instalacja
Zaleca się użycie środowiska wirtualnego, szczególnie na systemach macOS i Linux:

1. Stwórz środowisko wirtualne:
   ```bash
   python3 -m venv venv
   ```
2. Aktywuj środowisko:
   ```bash
   source venv/bin/activate
   ```
3. Zainstaluj wymagane biblioteki:
   ```bash
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

## Struktura projektu
```
src/
├── core/         # wczytywanie DICOM i model danych
├── interface/    # viewer (OpenCV)
├── interaction/  # input (voice – do zrobienia)
└── utils/        # przetwarzanie obrazu
```
