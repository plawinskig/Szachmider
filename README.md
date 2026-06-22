# Szachmider

Szachmider is a Polish chess game with a `pygame`-based interface, local SQLite score tracking, and a board editor.

## Features

- Main menu with animated elements and submenus
- Board selection from pre-defined templates
- Play against two bots: `Random Bot` and `Greedy Bot`
- Player results and game history stored in SQLite
- Statistics screen with player rankings
- Custom board editor with JSON save support
- Retro CRT visual effect

## Requirements

- Python 3.11 or newer
- `pygame-ce`
- `peewee`

## Installation

1. Open a terminal in the project folder.
2. (Optional) Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install required packages:

```powershell
python -m pip install -r requirements.txt
```

## Running the game

```powershell
python main.py
```

## Project structure

- `main.py` - main launcher for the game
- `source/board` - board logic, pieces, board view, and JSON save/load
- `source/game_logic` - game controller and gameplay rules
- `source/menu` - main menu and player/board selection menus
- `source/boardEditor` - board editor and selection tools
- `source/bot` - bot implementations
- `source/database` - SQLite database handling and Peewee models
- `source/statistics` - statistics screen and rankings
- `assets/` - images, icons, backgrounds, and GUI assets
- `boards/` - sample board JSON files

## Usage

- Select `Play` to configure players and piece colors.
- Select `Statistics` to view results and leaderboard.
- Select `Editor` to create or modify a board.

## Database

The game uses SQLite in the file `source/database/szachmider.db`.
The file `source/database/dbSetup.txt` contains the database schema setup commands.

## Notes

- The game runs in fullscreen mode.
- Make sure the `assets/` folder keeps its original structure.
