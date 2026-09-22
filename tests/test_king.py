from engine.board import Board
from engine.move_generator import MoveGenerator


def empty_board():
    board = Board()

    for row in range(8):
        for column in range(8):
            board.set_piece(row, column, Board.EMPTY)

    return board


def move_strings(moves):
    return [str(move) for move in moves]


def test_king_moves_in_all_directions():
    board = empty_board()
    board.set_piece(4, 4, "K")  # e4

    moves = MoveGenerator.generate_king_moves(board, "e4")

    assert set(move_strings(moves)) == {
        "e4d5",
        "e4e5",
        "e4f5",
        "e4d4",
        "e4f4",
        "e4d3",
        "e4e3",
        "e4f3",
    }


def test_king_can_capture_enemy_piece():
    board = empty_board()
    board.set_piece(4, 4, "K")  # e4
    board.set_piece(3, 5, "p")  # f5

    moves = MoveGenerator.generate_king_moves(board, "e4")

    assert "e4f5" in move_strings(moves)


def test_king_cannot_capture_own_piece():
    board = empty_board()
    board.set_piece(4, 4, "K")  # e4
    board.set_piece(3, 5, "P")  # f5

    moves = MoveGenerator.generate_king_moves(board, "e4")

    assert "e4f5" not in move_strings(moves)


def test_king_stays_inside_board():
    board = empty_board()
    board.set_piece(0, 0, "K")  # a8

    moves = MoveGenerator.generate_king_moves(board, "a8")

    assert set(move_strings(moves)) == {
        "a8b8",
        "a8a7",
        "a8b7",
    }


def test_black_king_moves():
    board = empty_board()
    board.set_piece(4, 4, "k")  # e4

    moves = MoveGenerator.generate_king_moves(board, "e4")

    assert len(moves) == 8


def test_king_requires_king_on_square():
    board = empty_board()

    try:
        MoveGenerator.generate_king_moves(board, "e4")
        assert False
    except ValueError:
        assert True