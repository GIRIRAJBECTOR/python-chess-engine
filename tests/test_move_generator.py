from engine.board import Board
from engine.move_generator import MoveGenerator


def move_strings(moves):
    return sorted(str(move) for move in moves)


def test_white_pawn_initial_moves():
    board = Board()

    moves = MoveGenerator.generate_pawn_moves(
        board,
        "e2"
    )

    assert move_strings(moves) == [
        "e2e3",
        "e2e4",
    ]


def test_black_pawn_initial_moves():
    board = Board()

    moves = MoveGenerator.generate_pawn_moves(
        board,
        "e7"
    )

    assert move_strings(moves) == [
        "e7e5",
        "e7e6",
    ]


def test_white_pawn_single_move():
    board = Board()

    board.set_piece(6, 4, ".")
    board.set_piece(5, 4, "P")

    moves = MoveGenerator.generate_pawn_moves(
        board,
        "e3"
    )

    assert move_strings(moves) == [
        "e3e4",
    ]


def test_pawn_cannot_move_forward_if_blocked():
    board = Board()

    board.set_piece(5, 4, "p")

    moves = MoveGenerator.generate_pawn_moves(
        board,
        "e2"
    )

    assert moves == []


def test_white_pawn_can_capture():
    board = Board()

    board.set_piece(6, 4, ".")
    board.set_piece(3, 4, "P")

    board.set_piece(2, 3, "p")
    board.set_piece(2, 5, "n")

    moves = MoveGenerator.generate_pawn_moves(
        board,
        "e5"
    )

    assert move_strings(moves) == [
        "e5d6",
        "e5e6",
        "e5f6",
    ]


def test_white_pawn_cannot_capture_own_piece():
    board = Board()

    board.set_piece(6, 4, ".")
    board.set_piece(3, 4, "P")

    board.set_piece(2, 3, "p")
    board.set_piece(2, 5, "N")

    moves = MoveGenerator.generate_pawn_moves(
        board,
        "e5"
    )

    assert move_strings(moves) == [
        "e5d6",
        "e5e6",
    ]


def test_pawn_cannot_double_move_after_leaving_start():
    board = Board()

    board.set_piece(6, 4, ".")
    board.set_piece(4, 4, "P")

    moves = MoveGenerator.generate_pawn_moves(
        board,
        "e4"
    )

    assert move_strings(moves) == [
        "e4e5",
    ]