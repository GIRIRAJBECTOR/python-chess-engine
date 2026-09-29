# Python Chess Engine

A custom chess engine built in Python with a playable Pygame interface, legal move generation, game-state handling, and a lightweight chess AI.

## Overview

This project was built from the ground up to explore chess-engine architecture, move generation, game-state management, search algorithms, automated testing, and GUI integration.

The current release is treated as **v1.0**.

## Features

### Chess Engine
- Board and game-state representation
- Legal move generation
- Piece movement and captures
- Check and checkmate detection
- Stalemate detection
- Pawn promotion
- FEN-based position loading
- Move history and undo support

### AI
- Minimax-style recursive search
- Alpha-beta pruning
- Capture-first move ordering
- Material-based evaluation
- Positional evaluation using piece-square tables
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
- The engine waits 5 seconds after the human move before calculating/playing its response

### Human vs Human
- Both sides are controlled by the players
- AI is disabled

## Project Structure

```text
python-chess-engine/
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

Run the complete test suite with:

```powershell
python -m pytest
```

At the v1.0 final checkpoint, the project test suite reported:

```text
144 passed
```

The test suite covers core engine behavior, move generation, board/game-state logic, piece movement, sliding pieces, perft, and AI behavior.

## AI Architecture

The AI uses a depth-limited recursive search.

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

The evaluation combines:

- Material values
- Piece-square tables
- Mobility
- Center occupancy

Material remains the dominant component so that positional bonuses do not outweigh major material differences.

## Testing Philosophy

The project uses `pytest` to validate the engine while new functionality is added.

Tests are organized by responsibility:

- Board representation
- Coordinates
- Individual piece movement
- Sliding-piece movement
- King behavior
- Move generation
- Game-state behavior
- Attack detection
- Perft
- AI

This makes it possible to modify the engine while continuously checking that existing behavior remains stable.

## Current Release Scope

**Version:** `1.0`

The v1.0 release focuses on a working playable engine rather than implementing every advanced chess-engine feature.

The architecture is intentionally modular so future work can be added without redesigning the whole project.

## Possible Future Improvements

- Expanded chess-rule coverage
- More complete draw-rule handling
- Stronger AI search
- Transposition tables
- Additional move-ordering heuristics
- Multiple AI difficulty levels
- Player-side selection
- Opening book
- PGN export/import
- FEN import/export improvements
- Game clock
- Save/load games
- Additional GUI polish

## Technologies

- **Python**
- **Pygame**
- **pytest**
- Git / GitHub

## Project Status

**v1.0 — Complete**

The current release is considered the finished baseline version of the project. Future enhancements can be developed as a separate v2.x line without changing the v1.0 scope.

## License

Add the license of your choice before publishing the project for external reuse.
