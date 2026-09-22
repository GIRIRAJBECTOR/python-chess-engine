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