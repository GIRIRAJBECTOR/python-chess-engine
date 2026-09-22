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