from engine.board import Board
from engine.move_generator import MoveGenerator


def move_strings(moves):
    return sorted(str(move) for move in moves)


def test_knight_initial_moves():
    board = Board()

    moves = MoveGenerator.generate_knight_moves(
        board,
        "g1"
    )

    assert move_strings(moves) == [
        "g1e2",
        "g1h3",
    ]


def test_knight_can_jump_over_pieces():
    board = Board()

    moves = MoveGenerator.generate_knight_moves(
        board,
        "b1"
    )

    assert move_strings(moves) == [
        "b1a3",
        "b1c3",
    ]


def test_knight_can_capture():
    board = Board()

    board.set_piece(7, 6, ".")
    board.set_piece(4, 4, "N")

    board.set_piece(2, 3, "p")
    board.set_piece(2, 5, "b")

    moves = MoveGenerator.generate_knight_moves(
        board,
        "e4"
    )

    moves = move_strings(moves)

    assert "e4d6" in moves
    assert "e4f6" in moves


def test_knight_cannot_capture_own_piece():
    board = Board()

    board.set_piece(7, 6, ".")
    board.set_piece(4, 4, "N")

    board.set_piece(2, 3, "P")

    moves = MoveGenerator.generate_knight_moves(
        board,
        "e4"
    )

    assert "e4d6" not in move_strings(moves)


def test_knight_edge_of_board():
    board = Board()

    board.set_piece(7, 6, ".")
    board.set_piece(7, 0, "N")

    moves = MoveGenerator.generate_knight_moves(
        board,
        "a1"
    )

    assert move_strings(moves) == [
        "a1b3",
        "a1c2",
    ]