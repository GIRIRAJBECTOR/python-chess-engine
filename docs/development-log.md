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