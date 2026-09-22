import pytest

from engine.board import Board
from engine.move_generator import MoveGenerator


def empty_board():
    board = Board()

    for row in range(8):
        for column in range(8):
            board.set_piece(row, column, Board.EMPTY)

    return board


def test_bishop_moves_on_empty_board():
    board = empty_board()
    board.set_piece(4, 4, "B")  # e4

    moves = MoveGenerator.generate_bishop_moves(board, "e4")

    actual = {str(move) for move in moves}

    expected = {
        "e4d5",
        "e4c6",
        "e4b7",
        "e4a8",
        "e4f5",
        "e4g6",
        "e4h7",
        "e4d3",
        "e4c2",
        "e4b1",
        "e4f3",
        "e4g2",
        "e4h1",
    }

    assert actual == expected


def test_bishop_stops_at_blocking_piece():
    board = empty_board()

    board.set_piece(4, 4, "B")  # e4
    board.set_piece(2, 2, "P")  # c6

    moves = MoveGenerator.generate_bishop_moves(board, "e4")

    actual = {str(move) for move in moves}

    assert "e4d5" in actual
    assert "e4c6" not in actual
    assert "e4b7" not in actual
    assert "e4a8" not in actual


def test_bishop_can_capture_enemy_piece():
    board = empty_board()

    board.set_piece(4, 4, "B")  # e4
    board.set_piece(2, 2, "p")  # c6

    moves = MoveGenerator.generate_bishop_moves(board, "e4")

    actual = {str(move) for move in moves}

    assert "e4c6" in actual
    assert "e4b7" not in actual


def test_bishop_cannot_capture_own_piece():
    board = empty_board()

    board.set_piece(4, 4, "B")  # e4
    board.set_piece(2, 2, "P")  # c6

    moves = MoveGenerator.generate_bishop_moves(board, "e4")

    actual = {str(move) for move in moves}

    assert "e4c6" not in actual


def test_rook_moves_on_empty_board():
    board = empty_board()
    board.set_piece(4, 4, "R")  # e4

    moves = MoveGenerator.generate_rook_moves(board, "e4")

    actual = {str(move) for move in moves}

    expected = {
        "e4e1",
        "e4e2",
        "e4e3",
        "e4e5",
        "e4e6",
        "e4e7",
        "e4e8",
        "e4a4",
        "e4b4",
        "e4c4",
        "e4d4",
        "e4f4",
        "e4g4",
        "e4h4",
    }

    assert actual == expected


def test_rook_stops_at_blocking_piece():
    board = empty_board()

    board.set_piece(4, 4, "R")  # e4
    board.set_piece(4, 6, "P")  # g4

    moves = MoveGenerator.generate_rook_moves(board, "e4")

    actual = {str(move) for move in moves}

    assert "e4f4" in actual
    assert "e4g4" not in actual
    assert "e4h4" not in actual


def test_rook_can_capture_enemy_piece():
    board = empty_board()

    board.set_piece(4, 4, "R")  # e4
    board.set_piece(4, 6, "p")  # g4

    moves = MoveGenerator.generate_rook_moves(board, "e4")

    actual = {str(move) for move in moves}

    assert "e4f4" in actual
    assert "e4g4" in actual
    assert "e4h4" not in actual


def test_queen_combines_bishop_and_rook_movement():
    board = empty_board()
    board.set_piece(4, 4, "Q")  # e4

    moves = MoveGenerator.generate_queen_moves(board, "e4")

    actual = {str(move) for move in moves}

    assert "e4e1" in actual
    assert "e4e8" in actual
    assert "e4a4" in actual
    assert "e4h4" in actual

    assert "e4d5" in actual
    assert "e4c6" in actual
    assert "e4b7" in actual
    assert "e4a8" in actual

    assert "e4f5" in actual
    assert "e4g6" in actual
    assert "e4h7" in actual


def test_sliding_piece_requires_piece_on_square():
    board = empty_board()

    with pytest.raises(ValueError):
        MoveGenerator.generate_bishop_moves(board, "e4")

    with pytest.raises(ValueError):
        MoveGenerator.generate_rook_moves(board, "e4")

    with pytest.raises(ValueError):
        MoveGenerator.generate_queen_moves(board, "e4")