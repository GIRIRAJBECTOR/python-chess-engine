# Development Log

## Stage 1 — Board Representation

Implemented an 8x8 board representation using a two-dimensional Python list.

The initial board position contains all 32 chess pieces.

### Testing

Added tests for:

- Initial piece placement
- Empty squares
- Updating board squares

---

## Stage 2 — Coordinate System

Implemented conversion between standard chess notation and internal row/column coordinates.

Examples:

- e4 -> (4, 4)
- (4, 4) -> e4

Added round-trip and invalid-coordinate tests.

---

## Stage 3 — Move Representation

Created a dedicated Move data model containing:

- Source square
- Destination square
- Optional promotion piece

---

## Stage 4 — Pawn Move Generation

Implemented pseudo-legal pawn movement:

- One-square movement
- Initial two-square movement
- Diagonal captures
- Blocked-pawn handling

Added automated tests for the above cases.

---

## Stage 5 — Knight Move Generation

Implemented pseudo-legal knight movement:

- L-shaped movement
- Captures
- Own-piece blocking
- Board boundaries
- Jumping over pieces

Added automated tests.

### Testing

22 tests passing at this milestone.

---

## Stage 6 — Sliding Piece Move Generation

Implemented pseudo-legal movement for sliding chess pieces.

### Sliding Move Algorithm

Added a reusable sliding-piece movement algorithm that follows a piece along one or more directions until it reaches the edge of the board or an occupied square.

The algorithm:

- Adds empty squares as valid destinations
- Allows captures of opponent pieces
- Stops when an occupied square is reached
- Does not allow capturing own pieces
- Prevents movement beyond blocking pieces

### Bishop

Implemented diagonal movement in four directions:

- Up-left
- Up-right
- Down-left
- Down-right

### Rook

Implemented horizontal and vertical movement:

- Up
- Down
- Left
- Right

### Queen

Implemented queen movement by combining:

- Bishop diagonal directions
- Rook horizontal and vertical directions

### Testing

Added automated tests covering:

- Bishop movement on an empty board
- Bishop blocking
- Bishop captures
- Bishop own-piece blocking
- Rook movement
- Rook blocking
- Rook captures
- Queen movement
- Invalid sliding-piece positions

31 tests passing at this milestone.

---

## Stage 7 — King Move Generation

Implemented basic pseudo-legal movement for the king.

### King Movement

The king can move one square in any of the eight directions:

- Up
- Down
- Left
- Right
- Four diagonals

The implementation:

- Allows movement to empty squares
- Allows captures of opponent pieces
- Prevents capturing own pieces
- Prevents movement outside the board

### Scope

King safety was intentionally handled in the later game-state/rules phase. The early move generator did not yet prevent a king from moving into an attacked square.

### Testing

Added tests covering:

- All eight king directions
- Enemy captures
- Own-piece blocking
- Board boundaries
- Black king movement
- Invalid king positions

37 tests passing at this milestone.

### Phase 1 Completion

With king movement implemented, basic movement generation existed for all six chess piece types:

- Pawn
- Knight
- Bishop
- Rook
- Queen
- King

**Phase 1 — Chess Core Foundation is complete.**

---

# Phase 2 — Game State and Legal Chess Rules

Completed the core game-state layer and legal chess rule handling.

### Implemented

- Game state and side-to-move tracking
- Move execution and undo functionality
- Captures
- Check detection
- Legal move generation
- Checkmate detection
- Stalemate detection
- Castling with castling-right tracking
- En passant
- Pawn promotion to Queen, Rook, Bishop, and Knight
- FEN position loading
- Halfmove and fullmove counters
- State snapshots for reliable undo/perft traversal
- Protection against capturing the king

### Validation

- Initial position Perft depth 1: 20
- Initial position Perft depth 2: 400
- Initial position Perft depth 3: 8,902
- Initial position Perft depth 4: 197,281
- Standard/special-position Perft validation

140 automated tests were passing at the Phase 2 completion checkpoint.

**Phase 2 is complete and ready for the GUI layer.**

---

# Phase 3 — GUI and AI

Implemented the playable graphical and computer-opponent layer.

### GUI

- Pygame chess board
- Piece selection and movement
- Legal-move interaction
- Move history
- Undo
- Restart
- Check/checkmate/stalemate status
- Game-mode selection

### Game Modes

Added:

- Computer vs Human
- Human vs Human

### AI

Implemented a depth-limited chess AI with:

- Alpha-beta search
- Move ordering
- Material evaluation
- Piece-square positional evaluation
- Mobility evaluation
- Center-control evaluation

### AI Turn Delay

Added a non-blocking 5-second delay after the human move before the computer makes its move.

The delay is handled through the GUI event loop so the application remains responsive.

### Final Validation

At the final v1.0 checkpoint:

**144 tests passed.**

The final release was committed and pushed to GitHub.

**Phase 3 — GUI and AI is complete.**

---

# Final Project Status

## Python Chess Engine v1.0

The project reached a stable, playable v1.0 release with:

- Core chess engine
- Legal chess rules
- Castling
- En passant
- Promotion
- FEN support
- Perft validation
- Undo/restart
- Pygame GUI
- Human vs Human
- Computer vs Human
- Chess AI
- Automated test coverage
- 144 passing tests

Future work can be developed as a separate v2.x line.
