# Bugs and Fixes

## Pawn Capture Test Failure

### Problem

A pawn capture test initially failed because the expected result
only included diagonal captures.

### Actual Result

The engine generated:

- e5d6
- e5e6
- e5f6

### Investigation

The pawn was correctly allowed to move forward from e5 to e6
because that square was empty.

The implementation was correct. The test expectation was
incorrect.

### Resolution

The test was updated to include the valid forward move.

### Lesson

A failing test does not automatically mean the implementation
is wrong. The expected behavior must also be validated against
the rules being implemented.

---

## Knight Test Expectation Corrections

### Problem

Two existing knight tests contained incorrect expected moves.

The tests expected knights to move onto squares occupied by their own
pieces.

### Investigation

In the initial position:

- `g1e2` is invalid because `e2` contains a white pawn.
- `g1f3` and `g1h3` are valid.

Similarly, from `a1`:

- `a1b3` is valid.
- `a1c2` is blocked by the white pawn on `c2`.

### Resolution

Updated the test expectations to match the actual chess movement rules.

### Lesson

Test expectations must account for board occupancy and piece ownership,
not only the geometric movement pattern of a piece.


## Phase 2 Fixes

### Circular import in attack detection
attack_detector.py accidentally imported GameState, while game_state.py already imported AttackDetector. This caused a circular import during test collection.

**Fix:** Removed the unnecessary GameState import from attack_detector.py.

### Standard Perft position mismatch
The initial Kiwipete Perft test used an incorrect FEN position, resulting in 45 moves instead of the expected 48.

**Fix:** Replaced the test position with the correct standard Kiwipete FEN.

### King capture handling
Move execution initially allowed an opponent king to be treated as a capturable piece.

**Fix:** make_move() now rejects attempts to capture a king. Checkmate remains the terminal condition instead.

### FEN support
Added FEN parsing to allow validation against standard chess positions and make the engine easier to test with arbitrary positions.

### Test validation
After the fixes, the complete test suite passed with 140 tests.
