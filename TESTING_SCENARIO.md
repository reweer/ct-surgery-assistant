# Scenariusz Testowy: Nawigacja po Slicach (Głosowa i Klawiszowa)

Scenariusz testowania funkcji poruszania się po obrazach tomografii komputerowej.

## 1. Przygotowanie
1. **Środowisko:** Upewnij się, że wirtualne środowisko jest aktywne:
   ```bash
   source venv/bin/activate
   ```
2. **Model Głosowy:** Sprawdź, czy model Vosk znajduje się w `models/vosk-model-small-en-us-0.15`.
3. **Uruchomienie:**
   ```bash
   python3 src/main.py --study 1
   ```

## 2. Testy Klawiszowe (Szybka weryfikacja)
Upewnij się, że okno aplikacji jest aktywne:
- [ ] Naciśnij **D**: Powinien wyświetlić się następny slice (licznik w rogu: `Slice: X / Y`).
- [ ] Naciśnij **A**: Powinien wyświetlić się poprzedni slice.
- [ ] Naciśnij **1**: Przełącz okno na kostne (Bone).
- [ ] Naciśnij **2**: Przełącz okno na tkanki miękkie (Soft).

## 3. Testy Głosowe (Podstawowe)
Wydaj komendy do mikrofonu (w języku angielskim):
- [ ] Powiedz: **"next"** -> Przeskok o +1 slice.
- [ ] Powiedz: **"previous"** lub **"back"** -> Przeskok o -1 slice.

## 4. Testy Głosowe (Skoki o wartość)
- [ ] Powiedz: **"next five"** lub **"next 5"** -> Przeskok o +5 sliców.
- [ ] Powiedz: **"back five"** lub **"previous 5"** -> Przeskok o -5 sliców.
- [ ] Powiedz: **"next ten"** -> Przeskok o +10 sliców.

## 5. Testy Głosowe (Skoki bezwzględne)
- [ ] Powiedz: **"slice ten"** -> Powinien pokazać się dokładnie 10. slice (licznik: `Slice: 10 / Y`).
- [ ] Powiedz: **"slice fifty"** (jeśli badanie ma tyle sliców) lub inna liczba.

## 6. Testy Graniczne (Kluczowe)
- [ ] Powiedz: **"first slice"** -> Skok do pierwszego obrazu (1).
- [ ] Powiedz: **"last slice"** -> Skok do ostatniego dostępnego obrazu.
- [ ] Powiedz: **"middle slice"** -> Powrót do środka badania.

## 7. Ograniczenia i Bezpieczeństwo
- [ ] Będąc na pierwszym slicie, powiedz **"back"** -> Aplikacja nie powinna się zamknąć, powinna zostać na 1.
- [ ] Będąc na ostatnim slicie, powiedz **"next"** -> Powinna zostać na ostatnim.
- [ ] Powiedz **"slice one thousand"** (liczba poza zakresem) -> Powinna zatrzymać się na ostatnim slicie.

## 8. Problemy?
- Jeśli głos nie reaguje: Sprawdź w terminalu, czy pojawia się komunikat `You said: ...`.
- Jeśli ścieżka do modelu jest inna: Popraw ją w `src/interaction/voice.py`.
