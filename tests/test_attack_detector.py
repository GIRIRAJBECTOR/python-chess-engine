from engine.board import Board
from engine.attack_detector import AttackDetector


def empty_board():
    board = Board()

    for row in range(8):
        for column in range(8):
            board.set_piece(row, column, Board.EMPTY)

    return board


def test_white_pawn_attack():
    board = empty_board()

    board.set_piece(4, 4, "P")  # e4

    assert AttackDetector.is_square_attacked(
        board, "d5", "white"
    )

    assert AttackDetector.is_square_attacked(
        board, "f5", "white"
    )

    assert not AttackDetector.is_square_attacked(
        board, "e5", "white"
    )


def test_black_pawn_attack():
    board = empty_board()

    board.set_piece(3, 4, "p")  # e5

    assert AttackDetector.is_square_attacked(
        board, "d4", "black"
    )

    assert AttackDetector.is_square_attacked(
        board, "f4", "black"
    )

    assert not AttackDetector.is_square_attacked(
        board, "e4", "black"
    )


def test_knight_attack():
    board = empty_board()

    board.set_piece(4, 4, "N")  # e4

    assert AttackDetector.is_square_attacked(
        board, "c5", "white"
    )

    assert AttackDetector.is_square_attacked(
        board, "f6", "white"
    )

    assert not AttackDetector.is_square_attacked(
        board, "e6", "white"
    )


def test_bishop_attack():
    board = empty_board()

    board.set_piece(4, 4, "B")  # e4

    assert AttackDetector.is_square_attacked(
        board, "h7", "white"
    )

    assert AttackDetector.is_square_attacked(
        board, "b7", "white"
    )

    assert not AttackDetector.is_square_attacked(
        board, "e7", "white"
    )


def test_bishop_attack_is_blocked():
    board = empty_board()

    board.set_piece(4, 4, "B")  # e4
    board.set_piece(3, 3, "R")  # d5

    assert not AttackDetector.is_square_attacked(
        board, "c6", "white"
    )


def test_rook_attack():
    board = empty_board()

    board.set_piece(4, 4, "R")  # e4

    assert AttackDetector.is_square_attacked(
        board, "e8", "white"
    )

    assert AttackDetector.is_square_attacked(
        board, "a4", "white"
    )

    assert not AttackDetector.is_square_attacked(
        board, "h8", "white"
    )


def test_rook_attack_is_blocked():
    board = empty_board()

    board.set_piece(4, 4, "R")  # e4
    board.set_piece(4, 5, "P")  # f4

    assert not AttackDetector.is_square_attacked(
        board, "h4", "white"
    )


def test_queen_diagonal_attack():
    board = empty_board()

    board.set_piece(4, 4, "Q")  # e4

    assert AttackDetector.is_square_attacked(
        board, "h7", "white"
    )


def test_queen_straight_attack():
    board = empty_board()

    board.set_piece(4, 4, "Q")  # e4

    assert AttackDetector.is_square_attacked(
        board, "e8", "white"
    )

    assert AttackDetector.is_square_attacked(
        board, "a4", "white"
    )


def test_king_attack():
    board = empty_board()

    board.set_piece(4, 4, "K")  # e4

    assert AttackDetector.is_square_attacked(
        board, "d5", "white"
    )

    assert AttackDetector.is_square_attacked(
        board, "f3", "white"
    )

    assert not AttackDetector.is_square_attacked(
        board, "e6", "white"
    )


def test_black_attacks_are_detected():
    board = empty_board()

    board.set_piece(4, 4, "q")  # e4

    assert AttackDetector.is_square_attacked(
        board, "e8", "black"
    )

    assert AttackDetector.is_square_attacked(
        board, "h7", "black"
    )


def test_wrong_color_is_not_an_attack():
    board = empty_board()

    board.set_piece(4, 4, "B")  # e4

    assert not AttackDetector.is_square_attacked(
        board, "h7", "black"
    )


def test_invalid_color():
    board = empty_board()

    try:
        AttackDetector.is_square_attacked(
            board, "e4", "blue"
        )
        assert False
    except ValueError:
        assert True