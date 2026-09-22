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

