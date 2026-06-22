# Szachmider

Szachmider to polska gra szachowa z interfejsem opartym na `pygame`, zapisem wyników do lokalnej bazy SQLite oraz edytorem plansz.

## Funkcje

- menu główne z animowanymi elementami i podmenu
- wybór planszy z gotowych szablonów
- gra z dwoma botami: `Random Bot` i `Greedy Bot`
- zapis wyników graczy i rozgrywek w SQLite
- ekran statystyk i rankingów graczy
- edytor własnych plansz z zapisem do plików JSON
- retro efekt CRT

## Wymagania

- Python 3.11 lub nowszy
- `pygame-ce`
- `peewee`

## Instalacja

1. Otwórz terminal w katalogu projektu.
2. (Opcjonalnie) utwórz i aktywuj środowisko wirtualne:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Zainstaluj wymagane pakiety:

```powershell
python -m pip install -r requirements.txt
```

## Uruchamianie

```powershell
python main.py
```

## Struktura projektu

- `main.py` - główny plik uruchamiający grę
- `source/board` - logika planszy, figur, widok planszy i zapis JSON
- `source/game_logic` - kontroler gry i reguły rozgrywki
- `source/menu` - menu główne i podmenu wyboru graczy oraz planszy
- `source/boardEditor` - edytor plansz i narzędzia wyboru elementów
- `source/bot` - implementacje botów
- `source/database` - obsługa bazy danych SQLite i modele Peewee
- `source/statistics` - ekran statystyk i rankingów
- `assets/` - obrazy, ikony, tła oraz elementy GUI
- `boards/` - przykładowe pliki plansz JSON

## Użytkowanie

- Wybierz `Graj`, by ustawić graczy i kolor figur.
- Wybierz `Statystyki`, by zobaczyć wyniki i ranking.
- Wybierz `Edytor`, by stworzyć lub zmodyfikować planszę.

## Baza danych

Aplikacja korzysta z SQLite w pliku `source/database/szachmider.db`.
Plik `source/database/dbSetup.txt` zawiera polecenia tworzące schemat bazy.

## Uwagi

- Gra uruchamia się w trybie pełnoekranowym.
- Upewnij się, że katalog `assets/` zachowuje oryginalną strukturę.
