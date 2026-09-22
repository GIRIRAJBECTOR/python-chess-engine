from engine.board import Board


def test_initial_board():
    board = Board()

    assert board.get_piece(7, 0) == "R"
    assert board.get_piece(7, 4) == "K"
    assert board.get_piece(0, 4) == "k"
    assert board.get_piece(1, 0) == "p"


def test_empty_square():
    board = Board()

    assert board.get_piece(3, 3) == "."


def test_set_piece():
    board = Board()

    board.set_piece(3, 3, "Q")

    assert board.get_piece(3, 3) == "Q"