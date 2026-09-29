# Python Chess Engine

A custom chess engine built in Python with a playable Pygame interface, legal move generation, game-state handling, automated testing, and a lightweight chess AI.

The current release is **v1.0**.

## Overview

This project was built from the ground up to explore chess-engine architecture, move generation, game-state management, search algorithms, automated testing, and GUI integration.

## Features

### Chess Engine

- 8x8 board representation
- Coordinate conversion between chess notation and internal coordinates
- Legal move generation
- Piece movement and captures
- Check detection
- Checkmate detection
- Stalemate detection
- Castling with castling-right tracking
- En passant
- Pawn promotion to Queen, Rook, Bishop, and Knight
- FEN position loading
- Halfmove and fullmove counters
- Move history and undo support
- State snapshots for reliable undo/perft traversal
- Protection against capturing the king
- Perft validation against standard positions

### AI

- Depth-limited recursive search
- Alpha-beta pruning
- Capture-first move ordering
- Material evaluation
- Piece-square positional evaluation
- Mobility and center-control bonuses
- Configurable search depth
- Deterministic move selection

### GUI

- Pygame-based chess board
- Click-to-select pieces
- Legal-move highlighting
- Move history
- Restart and Undo controls
- Check/checkmate/stalemate status
- Game-mode selection at startup
- Human vs Human
- Computer vs Human
- 5-second delay before the AI makes its move

## Game Modes

When the application starts, you can choose:

### Computer vs Human

- Human plays White
- Computer plays Black
- The engine waits 5 seconds after the human move before playing its response

### Human vs Human

- Both sides are controlled by players
- AI is disabled

## Project Structure

```text
python-chess-engine/
│
├── docs/
│   ├── development-log.md
│   ├── bugs-and-fixes.md
│   
├── engine/
│   ├── __init__.py
│   ├── board.py
│   ├── game_state.py
│   ├── move.py
│   ├── move_generator.py
│   └── ai.py
│
├── gui/
│   ├── __init__.py
│   ├── board_renderer.py
│   └── game_window.py
│
├── tests/
│   ├── test_ai.py
│   ├── test_attack_detector.py
│   ├── test_board.py
│   ├── test_coordinates.py
│   ├── test_game_state.py
│   ├── test_king.py
│   ├── test_knight.py
│   ├── test_move.py
│   ├── test_move_generator.py
│   ├── test_perft.py
│   └── test_sliding_pieces.py
│
├── main.py
├── requirements.txt
├── DEVELOPMENT_LOG.md
├── BUGS_AND_FIXES.md
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/GIRIRAJBECTOR/python-chess-engine.git
cd python-chess-engine
```

### 2. Create a virtual environment

Windows PowerShell:

```powershell
py -3.13 -m venv .venv
```

### 3. Activate the environment

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution for the current session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate again:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```powershell
pip install -r requirements.txt
```

## Run the Game

```powershell
python main.py
```

The application opens with the game-mode selection screen.

## Run Tests

```powershell
python -m pytest
```

At the final v1.0 checkpoint:

```text
144 passed
```

The test suite covers core engine behavior, move generation, board/game-state logic, piece movement, sliding pieces, perft, and AI behavior.

## AI Architecture

```text
Current Position
       │
       ▼
Generate Legal Moves
       │
       ▼
Order Moves
(captures first)
       │
       ▼
Alpha-Beta Search
       │
       ├── Checkmate → mate score
       ├── Stalemate → draw score
       └── Depth limit → position evaluation
       │
       ▼
Best Move
```

The position evaluation uses:

- Material values
- Piece-square tables
- Mobility
- Center occupancy

Material remains the dominant component so positional bonuses do not outweigh major material differences.

## Testing Philosophy

The project uses `pytest` to validate the engine as functionality is added.

Tests cover:

- Board representation
- Coordinates
- Individual piece movement
- Sliding-piece movement
- King behavior
- Move generation
- Game-state behavior
- Attack detection
- Perft
- AI behavior

## Validation

The engine was validated using standard positions and Perft counts, including:

```text
Initial position:
Depth 1: 20
Depth 2: 400
Depth 3: 8,902
Depth 4: 197,281
```

The development log also records validation of special positions and chess-rule behavior.

## Current Release Scope

**Version: 1.0**

The v1.0 release is a playable chess-engine project with core legal chess rules, a Pygame GUI, a computer opponent, and an automated test suite.

The architecture is modular so future improvements can be added without redesigning the whole project.

## Possible Future Improvements

- Stronger AI search
- Transposition tables
- Additional move-ordering heuristics
- Multiple AI difficulty levels
- Player-side selection
- Opening book
- PGN export/import
- Game clock
- Save/load games
- Additional GUI polish

## Technologies

- **Python**
- **Pygame**
- **pytest**
- **Git / GitHub**

## Project Status

**v1.0 — Complete**



