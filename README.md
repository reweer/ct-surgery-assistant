# CT Surgery Assistant

Proste narzędzie do przeglądania skanów tomografii komputerowej (CT) w formacie DICOM z obsługą sterowania głosowego.

## Setup (pierwsze uruchomienie)

### 1. Sklonuj repozytorium
```bash
git clone https://github.com/reweer/ct-surgery-assistant.git
cd ct-surgery-assistant
```

### 2. Stwórz środowisko wirtualne
Zaleca się użycie środowiska wirtualnego:
```bash
python3 -m venv venv
```

### 3. Aktywuj środowisko i zainstaluj biblioteki
*Pamiętaj, aby przed uruchomieniem zawsze aktywować środowisko komendą `source venv/bin/activate`.*
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

## Konfiguracja danych
1. Folder `data` znajduje się w głównym katalogu projektu (`ct-surgery-assistant/data`).
2. Dane są zorganizowane w podfolderach:
   - `data/zatoki_1/DICOM`
   - `data/zatoki_2/DICOM`
   - `data/zatoki_3/DICOM`

*Uwaga: Pliki DICOM są ignorowane przez Git i nie zostaną wysłane do repozytorium.*

## Sterowanie Głosowe (Model VOSK)
Projekt wymaga modelu VOSK. Możesz go pobrać i wypakować za pomocą poniższych komend:

```bash
mkdir -p models
curl -L https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip -o models/model.zip
unzip models/model.zip -d models/
```

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

## Sterowanie

### Klawiatura
| Klawisz | Funkcja |
|--------|--------|
| **a** | poprzedni slice |
| **d** | następny slice |
| **1** | okno kostne ($600 / 2000$ HU) – chirurgia kostna|
| **2** | tkanki miękkie ($40 / 400$ HU) – ocena błon śluzowych |
| **3** | tryb zatok ($300 / 2500$ HU) |
| **ESC** | wyjście |
| **+**   | powiększenie obrazu                   |
| **-**   | pomniejszenie obrazu                  |
| **↑**   | przesunięcie widoku w górę            |
| **↓**   | przesunięcie widoku w dół             |
| **←**   | przesunięcie widoku w lewo            |
| **→**   | przesunięcie widoku  w prawo          |
| **c**   | powrót do domyślnego widoku           |
| **ESC** | wyjście                               |

### Komendy Głosowe (Język Angielski)
Mów wyraźnie do mikrofonu po pojawieniu się komunikatu `🎤 Voice thread running...`.

| Komenda | Funkcja | Przykład |
|--------|--------|--------|
| **Next / Previous** | Przeskok o 1 slice | "next", "back" |
| **Next X / Back X** | Przeskok o X sliców | "next five", "back twenty" |
| **Slice X** | Skok do konkretnego numeru | "slice fifty", "slice 10" |
| **First / Last / Middle** | Skok do granic badania | "first slice", "middle slice" |
| **Bone / Soft / Sinus** | Zmiana okna widoku | "bone", "soft", "sinus" |
| **Brighter / Darker** | Płynna zmiana jasności o $50$ HU | "brighter" ,"darker" |
| **Contrast up / Contrast down** | Płynna zmiana kontrastu o $100$ HU | "contrast up" ,"contrast up" |
| **Zoom in**               | Powiększenie obrazu                         | "zoom in"                     |
| **Zoom out**              | Pomniejszenie obrazu                        | "zoom out"                    |
| **Left**                  | Przesunięcie widoku w lewo                  | "left"                        |
| **Right**                 | Przesunięcie widoku w prawo                 | "right"                       |
| **Up**                    | Przesunięcie widoku w górę                  | "up"                          |
| **Down**                  | Przesunięcie widoku w dół                   | "down"                        |
| **Center**                | Powrót do domyślnego widoku (środek obrazu) | "center"                      |



### Parser komend głosowych

System zawiera warstwę parsera komend, która:
	•	normalizuje tekst wejściowy,
	•	ignoruje wybrane słowa typu go, please, to,
	•	obsługuje liczby zapisane cyframi i słownie,
	•	mapuje część typowych błędów rozpoznawania mowy,
	•	zamienia komendę na ustandaryzowaną akcję.

Przykłady
	•	go next please → next
	•	next five → ruch o +5
	•	back ten → ruch o -10
	•	slice 120 → skok do slice’a 120
	•	zoom in a lot → szybsze powiększenie

### Obsługiwane liczby słownie

Obsługiwane są podstawowe liczby słownie, m.in.:
	•	zero–nineteen
	•	twenty, thirty, …, ninety
	•	hundred
	•	thousand


## Testowanie
1. Skrypt testowy nawigacji:
```bash
python3 tests/test_navigation.py
```
Pełen scenariusz testowy (manualny) znajduje się w pliku `TESTING_SCENARIO.md`.

2. Test parsera:
```bash
pytest tests/test_parser.py -v
```

3. Test integracyjny komend głosowych:
```bash
python3 tests/test_navigation.py
```

## Struktura projektu
```
src/
├── core/         # wczytywanie DICOM, model danych i kontroler
├── interface/    # viewer (PySide6)
├── interaction/  # obsługa głosu (Vosk)
└── utils/        # przetwarzanie obrazu
```

Dodatkowe Pliki:
```
tests/
├── test_navigation.py
├── test_parser.py
└── test_voice_integration.py

setup_audio.py
config.json
testing_scenario.md
```