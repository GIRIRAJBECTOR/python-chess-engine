# Development Log

## Stage 1 — Board Representation

Implemented an 8x8 board representation using a two-dimensional
Python list.

The initial board position contains all 32 chess pieces.

### Testing

Added tests for:

- Initial piece placement
- Empty squares
- Updating board squares

---

## Stage 2 — Coordinate System

Implemented conversion between standard chess notation and
internal row/column coordinates.

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

The current implementation:

- Allows movement to empty squares.
- Allows captures of opponent pieces.
- Prevents capturing own pieces.
- Prevents movement outside the board.

### Scope

King safety is intentionally not handled at this stage.

The current move generator does not yet prevent a king from moving into
an attacked square. Check detection and legal move filtering will be
implemented in the game-state/rules phase.

### Testing

Added tests covering:

- All eight king directions
- Enemy captures
- Own-piece blocking
- Board boundaries
- Black king movement
- Invalid king positions

Current test status:

**37 tests passing.**

### Phase 1 Completion

With king movement implemented, basic movement generation exists for all
six chess piece types:

- Pawn
- Knight
- Bishop
- Rook
- Queen
- King

Phase 1 — Chess Core Foundation is complete.


Implemented pseudo-legal knight movement:

- L-shaped movement
- Captures
- Own-piece blocking
- Board boundaries
- Jumping over pieces

Added automated tests.

### Current Test Status

22 tests passing.

---

## Stage 6 — Sliding Piece Move Generation

Implemented pseudo-legal movement for sliding chess pieces.

### Sliding Move Algorithm

Added a reusable sliding-piece movement algorithm that follows a piece
along one or more directions until it reaches the edge of the board or
an occupied square.

The algorithm:

- Adds empty squares as valid destinations.
- Allows captures of opponent pieces.
- Stops when an occupied square is reached.
- Does not allow capturing own pieces.
- Prevents movement beyond blocking pieces.

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

Current test status:

**31 tests passing.**

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

The current implementation:

- Allows movement to empty squares.
- Allows captures of opponent pieces.
- Prevents capturing own pieces.
- Prevents movement outside the board.

### Scope

King safety is intentionally not handled at this stage.

The current move generator does not yet prevent a king from moving into
an attacked square. Check detection and legal move filtering will be
implemented in the game-state/rules phase.

### Testing

Added tests covering:

- All eight king directions
- Enemy captures
- Own-piece blocking
- Board boundaries
- Black king movement
- Invalid king positions

Current test status:

**37 tests passing.**

### Phase 1 Completion

With king movement implemented, basic movement generation exists for all
six chess piece types:

- Pawn
- Knight
- Bishop
- Rook
- Queen
- King

Phase 1 — Chess Core Foundation is complete.

## Phase 2 ? Game State and Legal Chess Rules

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
- 140 automated tests passing

Phase 2 is complete and ready for the GUI layer.
