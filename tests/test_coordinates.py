import pytest

from engine.coordinates import (
    square_to_position,
    position_to_square,
)


def test_square_to_position():
    assert square_to_position("a8") == (0, 0)
    assert square_to_position("e4") == (4, 4)
    assert square_to_position("h1") == (7, 7)


def test_position_to_square():
    assert position_to_square(0, 0) == "a8"
    assert position_to_square(4, 4) == "e4"
    assert position_to_square(7, 7) == "h1"


def test_round_trip_conversion():
    squares = ["a1", "b2", "e4", "f6", "h8"]

    for square in squares:
        row, column = square_to_position(square)
        assert position_to_square(row, column) == square


def test_invalid_square():
    with pytest.raises(ValueError):
        square_to_position("z9")


def test_invalid_position():
    with pytest.raises(ValueError):
        position_to_square(8, 0)