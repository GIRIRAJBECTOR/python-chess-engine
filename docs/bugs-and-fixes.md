# Bugs and Fixes

## Pawn Capture Test Failure

### Problem

A pawn capture test initially failed because the expected result only included diagonal captures.

### Actual Result

The engine generated:

- e5d6
- e5e6
- e5f6

### Investigation

The pawn was correctly allowed to move forward from e5 to e6 because that square was empty.

The implementation was correct. The test expectation was incorrect.

### Resolution

The test was updated to include the valid forward move.

### Lesson

A failing test does not automatically mean the implementation is wrong. The expected behavior must also be validated against the rules being implemented.

---

## Knight Test Expectation Corrections

### Problem

Two existing knight tests contained incorrect expected moves.

The tests expected knights to move onto squares occupied by their own pieces.

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

Test expectations must account for board occupancy and piece ownership, not only the geometric movement pattern of a piece.

---

## Phase 2 Fixes

### Circular import in attack detection

`attack_detector.py` accidentally imported `GameState`, while `game_state.py` already imported `AttackDetector`. This caused a circular import during test collection.

**Fix:** Removed the unnecessary `GameState` import from `attack_detector.py`.

### Standard Perft position mismatch

The initial Kiwipete Perft test used an incorrect FEN position, resulting in 45 moves instead of the expected 48.

**Fix:** Replaced the test position with the correct standard Kiwipete FEN.

### King capture handling

Move execution initially allowed an opponent king to be treated as a capturable piece.

**Fix:** `make_move()` now rejects attempts to capture a king. Checkmate remains the terminal condition instead.

### FEN support

Added FEN parsing to allow validation against standard chess positions and make the engine easier to test with arbitrary positions.

### Test validation

After the Phase 2 fixes, the complete test suite passed with 140 tests.

---

# Phase 3 — GUI and AI Fixes

## AI evaluation and search integration

### Problem

The AI needed to move beyond a basic material-only evaluation while keeping the existing search interface stable.

### Fix

Added positional evaluation using:

- Piece-square tables
- Mobility
- Center control
- Material weighting

The existing alpha-beta search and public AI interface were preserved.

### Validation

The AI changes were integrated without breaking the existing test suite.

---

## Five-second AI turn delay

### Requirement

The computer should wait 5 seconds after the human move before making its move.

### Fix

Implemented the delay through the Pygame event loop rather than `time.sleep()`.

This prevents the GUI from freezing while the AI is waiting.

### Result

The computer turn now follows:

```text
Human move
    ↓
5-second delay
    ↓
AI move
```

Human board interaction is locked while the AI is waiting or thinking.

---

## Game-mode selection

### Requirement

The application should allow the player to choose the game type when starting.

### Fix

Added a startup menu with:

- Computer vs Human
- Human vs Human

In Computer vs Human mode, the AI controls Black.

In Human vs Human mode, the AI is disabled.

---

# Final Validation

The final v1.0 project checkpoint reported:

```text
144 passed
```

The project was then committed and pushed to GitHub.

## Lessons

- Validate failing tests against the actual rules before changing implementation code.
- Keep engine logic separate from GUI logic.
- Use standard chess positions and Perft to validate move generation.
- Avoid blocking the GUI event loop for timed AI behavior.
- Keep the test suite running after every major engine or GUI change.
