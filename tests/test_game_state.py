import pytest

from engine.board import Board
from engine.game_state import GameState
from engine.move import Move


def empty_board():
    board = Board()

    for row in range(8):
        for column in range(8):
            board.set_piece(row, column, Board.EMPTY)

    return board


def test_initial_game_state():
    game = GameState()

    assert isinstance(game.board, Board)
    assert game.side_to_move == GameState.WHITE

    assert game.castling_rights == {
        "K": True,
        "Q": True,
        "k": True,
        "q": True,
    }

    assert game.en_passant_target is None
    assert game.halfmove_clock == 0
    assert game.fullmove_number == 1
    assert game.move_history == []


def test_switch_side():
    game = GameState()

    assert game.side_to_move == GameState.WHITE

    game.switch_side()

    assert game.side_to_move == GameState.BLACK

    game.switch_side()

    assert game.side_to_move == GameState.WHITE


def test_white_castling_rights():
    game = GameState()

    assert game.can_castle_kingside(GameState.WHITE)
    assert game.can_castle_queenside(GameState.WHITE)


def test_black_castling_rights():
    game = GameState()

    assert game.can_castle_kingside(GameState.BLACK)
    assert game.can_castle_queenside(GameState.BLACK)


def test_invalid_castling_color():
    game = GameState()

    with pytest.raises(ValueError):
        game.can_castle_kingside("blue")


def test_reset_en_passant():
    game = GameState()

    game.en_passant_target = "e3"

    assert game.en_passant_target == "e3"

    game.reset_en_passant()

    assert game.en_passant_target is None


def test_custom_board_can_be_used():
    board = Board()

    board.set_piece(6, 4, Board.EMPTY)

    game = GameState(board)

    assert game.board is board
    assert game.board.get_piece(6, 4) == Board.EMPTY


def test_make_white_pawn_move():
    game = GameState()

    captured_piece = game.make_move(
        Move("e2", "e4")
    )

    assert captured_piece == Board.EMPTY

    assert game.board.get_piece(6, 4) == Board.EMPTY
    assert game.board.get_piece(4, 4) == "P"

    assert game.side_to_move == GameState.BLACK
    assert game.move_history == [Move("e2", "e4")]
    assert game.halfmove_clock == 0
    assert game.fullmove_number == 1


def test_make_black_move_increments_fullmove_number():
    game = GameState()

    game.make_move(Move("e2", "e4"))
    game.make_move(Move("e7", "e5"))

    assert game.side_to_move == GameState.WHITE
    assert game.fullmove_number == 2


def test_capture_removes_piece():
    game = GameState()

    game.make_move(Move("e2", "e4"))
    game.make_move(Move("d7", "d5"))

    captured_piece = game.make_move(
        Move("e4", "d5")
    )

    assert captured_piece == "p"
    assert game.board.get_piece(3, 3) == "P"
    assert game.halfmove_clock == 0


def test_make_and_undo_restores_position():
    game = GameState()

    original_board = [row[:] for row in game.board.board]
    original_side = game.side_to_move
    original_fullmove = game.fullmove_number

    game.make_move(Move("e2", "e4"))

    game.undo_move()

    assert game.board.board == original_board
    assert game.side_to_move == original_side
    assert game.fullmove_number == original_fullmove
    assert game.move_history == []


def test_undo_restores_captured_piece():
    game = GameState()

    game.make_move(Move("e2", "e4"))
    game.make_move(Move("d7", "d5"))
    game.make_move(Move("e4", "d5"))

    assert game.board.get_piece(3, 3) == "P"

    game.undo_move()

    assert game.board.get_piece(3, 3) == "p"
    assert game.board.get_piece(4, 4) == "P"
    assert game.side_to_move == GameState.WHITE


def test_multiple_undo_operations():
    game = GameState()

    original_board = [row[:] for row in game.board.board]

    game.make_move(Move("e2", "e4"))
    game.make_move(Move("e7", "e5"))

    game.undo_move()
    game.undo_move()

    assert game.board.board == original_board
    assert game.side_to_move == GameState.WHITE
    assert game.move_history == []


def test_undo_without_move_raises_error():
    game = GameState()

    with pytest.raises(ValueError):
        game.undo_move()


def test_wrong_side_cannot_move():
    game = GameState()

    with pytest.raises(ValueError):
        game.make_move(Move("e7", "e5"))


def test_empty_source_square_raises_error():
    game = GameState()

    with pytest.raises(ValueError):
        game.make_move(Move("e4", "e5"))


def test_cannot_capture_own_piece():
    game = GameState()

    with pytest.raises(ValueError):
        game.make_move(Move("e2", "e1"))


# ------------------------------------------------------------------
# Check detection tests
# ------------------------------------------------------------------

def test_initial_position_is_not_in_check():
    game = GameState()

    assert not game.is_in_check(GameState.WHITE)
    assert not game.is_in_check(GameState.BLACK)


def test_white_king_in_check_by_rook():
    board = empty_board()

    board.set_piece(7, 4, "K")
    board.set_piece(0, 0, "k")
    board.set_piece(0, 4, "r")

    game = GameState(board)

    assert game.is_in_check(GameState.WHITE)
    assert not game.is_in_check(GameState.BLACK)


def test_black_king_in_check_by_rook():
    board = empty_board()

    board.set_piece(0, 4, "k")
    board.set_piece(7, 0, "K")
    board.set_piece(7, 4, "R")

    game = GameState(board)

    assert game.is_in_check(GameState.BLACK)
    assert not game.is_in_check(GameState.WHITE)


def test_white_king_in_check_by_knight():
    board = empty_board()

    board.set_piece(7, 4, "K")
    board.set_piece(5, 5, "n")
    board.set_piece(0, 0, "k")

    game = GameState(board)

    assert game.is_in_check(GameState.WHITE)
    assert not game.is_in_check(GameState.BLACK)


def test_black_king_in_check_by_bishop():
    board = empty_board()

    board.set_piece(0, 4, "k")
    board.set_piece(7, 0, "K")
    board.set_piece(3, 1, "B")

    game = GameState(board)

    assert game.is_in_check(GameState.BLACK)
    assert not game.is_in_check(GameState.WHITE)


def test_white_king_in_check_by_pawn():
    board = empty_board()

    board.set_piece(7, 4, "K")
    board.set_piece(6, 3, "p")
    board.set_piece(0, 0, "k")

    game = GameState(board)

    assert game.is_in_check(GameState.WHITE)
    assert not game.is_in_check(GameState.BLACK)


def test_black_king_in_check_by_pawn():
    board = empty_board()

    board.set_piece(0, 4, "k")
    board.set_piece(7, 0, "K")
    board.set_piece(1, 3, "P")

    game = GameState(board)

    assert game.is_in_check(GameState.BLACK)
    assert not game.is_in_check(GameState.WHITE)


def test_king_is_not_in_check_when_attack_is_blocked():
    board = empty_board()

    board.set_piece(7, 4, "K")
    board.set_piece(0, 4, "r")
    board.set_piece(4, 4, "P")
    board.set_piece(0, 0, "k")

    game = GameState(board)

    assert not game.is_in_check(GameState.WHITE)
    assert not game.is_in_check(GameState.BLACK)


def test_invalid_check_color():
    game = GameState()

    with pytest.raises(ValueError):
        game.is_in_check("blue")


def test_missing_king_raises_error():
    board = empty_board()

    game = GameState(board)

    with pytest.raises(ValueError):
        game.is_in_check(GameState.WHITE)


# ------------------------------------------------------------------
# Legal move generation tests
# ------------------------------------------------------------------

def test_initial_position_has_20_legal_moves():
    game = GameState()

    moves = game.generate_legal_moves()

    assert len(moves) == 20


def test_initial_position_has_20_white_pseudo_legal_moves():
    game = GameState()

    moves = game.generate_pseudo_legal_moves(GameState.WHITE)

    assert len(moves) == 20


def test_black_initial_position_has_20_legal_moves():
    game = GameState()

    moves = game.generate_legal_moves(GameState.BLACK)

    assert len(moves) == 20


def test_king_cannot_move_into_rook_attack():
    board = empty_board()

    board.set_piece(7, 4, "K")
    board.set_piece(0, 0, "k")
    board.set_piece(0, 4, "r")

    game = GameState(board)

    moves = game.generate_legal_moves(GameState.WHITE)

    move_strings = {str(move) for move in moves}

    assert "e1e2" not in move_strings


def test_pinned_piece_cannot_expose_king():
    board = empty_board()

    board.set_piece(7, 4, "K")
    board.set_piece(6, 4, "R")
    board.set_piece(0, 4, "r")
    board.set_piece(0, 0, "k")

    game = GameState(board)

    moves = game.generate_legal_moves(GameState.WHITE)

    move_strings = {str(move) for move in moves}

    assert "e2d2" not in move_strings
    assert "e2f2" not in move_strings


def test_check_can_be_blocked():
    board = empty_board()

    board.set_piece(7, 4, "K")
    board.set_piece(0, 0, "k")
    board.set_piece(0, 4, "r")
    board.set_piece(6, 3, "B")

    game = GameState(board)

    assert game.is_in_check(GameState.WHITE)

    moves = game.generate_legal_moves(GameState.WHITE)

    move_strings = {str(move) for move in moves}

    assert "d2e3" in move_strings


def test_king_can_capture_attacking_piece_when_safe():
    board = empty_board()

    board.set_piece(7, 4, "K")
    board.set_piece(0, 0, "k")
    board.set_piece(6, 4, "r")

    game = GameState(board)

    assert game.is_in_check(GameState.WHITE)

    moves = game.generate_legal_moves(GameState.WHITE)

    move_strings = {str(move) for move in moves}

    assert "e1e2" in move_strings


def test_legal_move_does_not_leave_king_in_check():
    board = empty_board()

    board.set_piece(7, 4, "K")
    board.set_piece(0, 0, "k")
    board.set_piece(0, 4, "r")
    board.set_piece(7, 3, "R")

    game = GameState(board)

    moves = game.generate_legal_moves(GameState.WHITE)

    for move in moves:
        game.make_move(move)

        assert not game.is_in_check(GameState.WHITE)

        game.undo_move()


# ------------------------------------------------------------------
# Checkmate and stalemate tests
# ------------------------------------------------------------------

def test_fools_mate_is_checkmate():
    game = GameState()

    game.make_move(Move("f2", "f3"))
    game.make_move(Move("e7", "e5"))
    game.make_move(Move("g2", "g4"))
    game.make_move(Move("d8", "h4"))

    assert game.side_to_move == GameState.WHITE
    assert game.is_in_check(GameState.WHITE)
    assert game.is_checkmate(GameState.WHITE)
    assert game.is_game_over()


def test_position_with_escape_move_is_not_checkmate():
    board = empty_board()

    board.set_piece(7, 4, "K")
    board.set_piece(0, 0, "k")
    board.set_piece(0, 4, "r")

    game = GameState(board)

    assert game.is_in_check(GameState.WHITE)
    assert not game.is_checkmate(GameState.WHITE)


def test_stalemate_position():
    board = empty_board()

    board.set_piece(0, 0, "k")
    board.set_piece(2, 2, "K")
    board.set_piece(2, 1, "Q")

    game = GameState(board)
    game.side_to_move = GameState.BLACK

    assert not game.is_in_check(GameState.BLACK)
    assert game.generate_legal_moves(GameState.BLACK) == []
    assert game.is_stalemate(GameState.BLACK)
    assert game.is_game_over()


def test_position_with_legal_move_is_not_stalemate():
    board = empty_board()

    board.set_piece(0, 0, "k")
    board.set_piece(7, 7, "K")

    game = GameState(board)

    assert not game.is_in_check(GameState.BLACK)
    assert not game.is_stalemate(GameState.BLACK)
    assert not game.is_game_over()


def test_checkmate_requires_check():
    board = empty_board()

    board.set_piece(7, 4, "K")
    board.set_piece(0, 0, "k")

    game = GameState(board)

    assert not game.is_in_check(GameState.WHITE)
    assert not game.is_checkmate(GameState.WHITE)


def test_stalemate_is_not_checkmate():
    board = empty_board()

    board.set_piece(0, 0, "k")
    board.set_piece(2, 2, "K")
    board.set_piece(2, 1, "Q")

    game = GameState(board)

    assert not game.is_in_check(GameState.BLACK)
    assert game.is_stalemate(GameState.BLACK)
    assert not game.is_checkmate(GameState.BLACK)


# ------------------------------------------------------------------
# Castling tests
# ------------------------------------------------------------------

def test_white_kingside_castling_is_legal():
    board = empty_board()

    board.set_piece(7, 4, "K")
    board.set_piece(7, 7, "R")
    board.set_piece(0, 4, "k")

    game = GameState(board)

    moves = game.generate_legal_moves(GameState.WHITE)
    move_strings = {str(move) for move in moves}

    assert "e1g1" in move_strings


def test_white_queenside_castling_is_legal():
    board = empty_board()

    board.set_piece(7, 4, "K")
    board.set_piece(7, 0, "R")
    board.set_piece(0, 4, "k")

    game = GameState(board)

    moves = game.generate_legal_moves(GameState.WHITE)
    move_strings = {str(move) for move in moves}

    assert "e1c1" in move_strings


def test_black_kingside_castling_is_legal():
    board = empty_board()

    board.set_piece(0, 4, "k")
    board.set_piece(0, 7, "r")
    board.set_piece(7, 4, "K")

    game = GameState(board)
    game.side_to_move = GameState.BLACK

    moves = game.generate_legal_moves(GameState.BLACK)
    move_strings = {str(move) for move in moves}

    assert "e8g8" in move_strings


def test_black_queenside_castling_is_legal():
    board = empty_board()

    board.set_piece(0, 4, "k")
    board.set_piece(0, 0, "r")
    board.set_piece(7, 4, "K")

    game = GameState(board)
    game.side_to_move = GameState.BLACK

    moves = game.generate_legal_moves(GameState.BLACK)
    move_strings = {str(move) for move in moves}

    assert "e8c8" in move_strings


def test_castling_moves_rook_and_king():
    board = empty_board()

    board.set_piece(7, 4, "K")
    board.set_piece(7, 7, "R")
    board.set_piece(0, 4, "k")

    game = GameState(board)

    game.make_move(Move("e1", "g1"))

    assert game.board.get_piece(7, 6) == "K"
    assert game.board.get_piece(7, 5) == "R"
    assert game.board.get_piece(7, 4) == Board.EMPTY
    assert game.board.get_piece(7, 7) == Board.EMPTY

    assert not game.can_castle_kingside(GameState.WHITE)
    assert not game.can_castle_queenside(GameState.WHITE)


def test_castling_rights_removed_when_king_moves():
    board = empty_board()

    board.set_piece(7, 4, "K")
    board.set_piece(7, 7, "R")
    board.set_piece(7, 0, "R")
    board.set_piece(0, 4, "k")

    game = GameState(board)

    game.make_move(Move("e1", "e2"))

    assert not game.can_castle_kingside(GameState.WHITE)
    assert not game.can_castle_queenside(GameState.WHITE)


def test_castling_right_removed_when_kingside_rook_moves():
    board = empty_board()

    board.set_piece(7, 4, "K")
    board.set_piece(7, 7, "R")
    board.set_piece(0, 4, "k")

    game = GameState(board)

    game.make_move(Move("h1", "h2"))

    assert not game.can_castle_kingside(GameState.WHITE)
    assert game.can_castle_queenside(GameState.WHITE)


def test_castling_right_removed_when_queenside_rook_moves():
    board = empty_board()

    board.set_piece(7, 4, "K")
    board.set_piece(7, 0, "R")
    board.set_piece(0, 4, "k")

    game = GameState(board)

    game.make_move(Move("a1", "a2"))

    assert not game.can_castle_queenside(GameState.WHITE)
    assert game.can_castle_kingside(GameState.WHITE)


def test_castling_not_allowed_when_piece_blocks_path():
    board = empty_board()

    board.set_piece(7, 4, "K")
    board.set_piece(7, 7, "R")
    board.set_piece(7, 5, "B")
    board.set_piece(0, 4, "k")

    game = GameState(board)

    moves = game.generate_legal_moves(GameState.WHITE)
    move_strings = {str(move) for move in moves}

    assert "e1g1" not in move_strings


def test_castling_not_allowed_when_king_is_in_check():
    board = empty_board()

    board.set_piece(7, 4, "K")
    board.set_piece(7, 7, "R")
    board.set_piece(0, 0, "k")
    board.set_piece(0, 4, "r")

    game = GameState(board)

    assert game.is_in_check(GameState.WHITE)

    moves = game.generate_legal_moves(GameState.WHITE)
    move_strings = {str(move) for move in moves}

    assert "e1g1" not in move_strings


def test_castling_not_allowed_through_attacked_square():
    board = empty_board()

    board.set_piece(7, 4, "K")
    board.set_piece(7, 7, "R")
    board.set_piece(0, 4, "k")
    board.set_piece(0, 5, "r")

    game = GameState(board)

    moves = game.generate_legal_moves(GameState.WHITE)
    move_strings = {str(move) for move in moves}

    assert "e1g1" not in move_strings


def test_castling_not_allowed_to_attacked_square():
    board = empty_board()

    board.set_piece(7, 4, "K")
    board.set_piece(7, 7, "R")
    board.set_piece(0, 4, "k")
    board.set_piece(0, 6, "r")

    game = GameState(board)

    moves = game.generate_legal_moves(GameState.WHITE)
    move_strings = {str(move) for move in moves}

    assert "e1g1" not in move_strings


def test_undo_castling_restores_position_and_rights():
    board = empty_board()

    board.set_piece(7, 4, "K")
    board.set_piece(7, 7, "R")
    board.set_piece(0, 4, "k")

    game = GameState(board)

    original_board = [row[:] for row in game.board.board]

    game.make_move(Move("e1", "g1"))

    game.undo_move()

    assert game.board.board == original_board
    assert game.side_to_move == GameState.WHITE

    assert game.can_castle_kingside(GameState.WHITE)
    assert game.can_castle_queenside(GameState.WHITE)


# ------------------------------------------------------------------
# En passant tests
# ------------------------------------------------------------------

def test_white_double_pawn_move_sets_en_passant_target():
    game = GameState()

    game.make_move(Move("e2", "e4"))

    assert game.en_passant_target == "e3"


def test_black_double_pawn_move_sets_en_passant_target():
    game = GameState()

    game.make_move(Move("e2", "e4"))
    game.make_move(Move("a7", "a5"))

    assert game.en_passant_target == "a6"


def test_en_passant_target_is_cleared_after_next_move():
    game = GameState()

    game.make_move(Move("e2", "e4"))

    assert game.en_passant_target == "e3"

    game.make_move(Move("a7", "a6"))

    assert game.en_passant_target is None


def test_white_can_capture_en_passant():
    board = empty_board()

    board.set_piece(7, 4, "K")
    board.set_piece(0, 4, "k")
    board.set_piece(3, 4, "P")
    board.set_piece(1, 3, "p")

    game = GameState(board)

    game.side_to_move = GameState.BLACK
    game.make_move(Move("d7", "d5"))

    assert game.en_passant_target == "d6"

    game.side_to_move = GameState.WHITE

    moves = game.generate_legal_moves(GameState.WHITE)
    move_strings = {str(move) for move in moves}

    assert "e5d6" in move_strings


def test_black_can_capture_en_passant():
    board = empty_board()

    board.set_piece(7, 4, "K")
    board.set_piece(0, 4, "k")
    board.set_piece(4, 4, "p")
    board.set_piece(6, 3, "P")

    game = GameState(board)

    game.side_to_move = GameState.WHITE
    game.make_move(Move("d2", "d4"))

    assert game.en_passant_target == "d3"

    game.side_to_move = GameState.BLACK

    moves = game.generate_legal_moves(GameState.BLACK)
    move_strings = {str(move) for move in moves}

    assert "e4d3" in move_strings


def test_white_en_passant_removes_captured_pawn():
    board = empty_board()

    board.set_piece(7, 4, "K")
    board.set_piece(0, 4, "k")
    board.set_piece(3, 4, "P")
    board.set_piece(3, 3, "p")

    game = GameState(board)

    game.side_to_move = GameState.BLACK
    game.make_move(Move("d5", "d4"))

    game.side_to_move = GameState.WHITE
    game.make_move(Move("e5", "d4"))

    assert game.board.get_piece(4, 3) == "P"
    assert game.board.get_piece(3, 3) == Board.EMPTY


def test_black_en_passant_removes_captured_pawn():
    board = empty_board()

    board.set_piece(7, 4, "K")
    board.set_piece(0, 4, "k")
    board.set_piece(4, 3, "P")
    board.set_piece(4, 4, "p")

    game = GameState(board)

    game.side_to_move = GameState.WHITE
    game.make_move(Move("d4", "d5"))

    game.side_to_move = GameState.BLACK
    game.make_move(Move("e4", "d3"))

    assert game.board.get_piece(5, 3) == "p"
    assert game.board.get_piece(4, 3) == Board.EMPTY


def test_en_passant_expires_after_one_move():
    board = empty_board()

    board.set_piece(7, 4, "K")
    board.set_piece(0, 4, "k")
    board.set_piece(3, 4, "P")
    board.set_piece(1, 3, "p")

    game = GameState(board)

    game.side_to_move = GameState.BLACK
    game.make_move(Move("d7", "d5"))

    assert game.en_passant_target == "d6"

    game.side_to_move = GameState.WHITE
    game.make_move(Move("e5", "e6"))

    assert game.en_passant_target is None


def test_undo_restores_en_passant_target():
    game = GameState()

    game.make_move(Move("e2", "e4"))

    assert game.en_passant_target == "e3"

    game.undo_move()

    assert game.en_passant_target is None
    assert game.board.get_piece(6, 4) == "P"
    assert game.board.get_piece(4, 4) == Board.EMPTY


# ------------------------------------------------------------------
# Promotion tests
# ------------------------------------------------------------------

def test_white_pawn_generates_four_promotion_moves():
    board = empty_board()

    board.set_piece(7, 4, "K")
    board.set_piece(0, 4, "k")
    board.set_piece(1, 0, "P")

    game = GameState(board)

    moves = game.generate_legal_moves(GameState.WHITE)

    move_strings = {str(move) for move in moves}

    assert "a7a8Q" in move_strings
    assert "a7a8R" in move_strings
    assert "a7a8B" in move_strings
    assert "a7a8N" in move_strings


def test_black_pawn_generates_four_promotion_moves():
    board = empty_board()

    board.set_piece(7, 4, "K")
    board.set_piece(0, 4, "k")
    board.set_piece(6, 0, "p")

    game = GameState(board)
    game.side_to_move = GameState.BLACK

    moves = game.generate_legal_moves(GameState.BLACK)

    move_strings = {str(move) for move in moves}

    assert "a2a1q" in move_strings
    assert "a2a1r" in move_strings
    assert "a2a1b" in move_strings
    assert "a2a1n" in move_strings


def test_white_pawn_promotes_to_queen():
    board = empty_board()

    board.set_piece(7, 4, "K")
    board.set_piece(0, 4, "k")
    board.set_piece(1, 0, "P")

    game = GameState(board)

    game.make_move(
        Move("a7", "a8", promotion="Q")
    )

    assert game.board.get_piece(0, 0) == "Q"
    assert game.board.get_piece(1, 0) == Board.EMPTY


def test_white_pawn_promotes_to_rook():
    board = empty_board()

    board.set_piece(7, 4, "K")
    board.set_piece(0, 4, "k")
    board.set_piece(1, 0, "P")

    game = GameState(board)

    game.make_move(
        Move("a7", "a8", promotion="R")
    )

    assert game.board.get_piece(0, 0) == "R"


def test_white_pawn_promotes_to_bishop():
    board = empty_board()

    board.set_piece(7, 4, "K")
    board.set_piece(0, 4, "k")
    board.set_piece(1, 0, "P")

    game = GameState(board)

    game.make_move(
        Move("a7", "a8", promotion="B")
    )

    assert game.board.get_piece(0, 0) == "B"


def test_white_pawn_promotes_to_knight():
    board = empty_board()

    board.set_piece(7, 4, "K")
    board.set_piece(0, 4, "k")
    board.set_piece(1, 0, "P")

    game = GameState(board)

    game.make_move(
        Move("a7", "a8", promotion="N")
    )

    assert game.board.get_piece(0, 0) == "N"


def test_black_pawn_promotes_to_queen():
    board = empty_board()

    board.set_piece(7, 4, "K")
    board.set_piece(0, 4, "k")
    board.set_piece(6, 0, "p")

    game = GameState(board)
    game.side_to_move = GameState.BLACK

    game.make_move(
        Move("a2", "a1", promotion="q")
    )

    assert game.board.get_piece(7, 0) == "q"


def test_promotion_capture():
    board = empty_board()

    board.set_piece(7, 4, "K")
    board.set_piece(0, 4, "k")
    board.set_piece(1, 0, "P")
    board.set_piece(0, 1, "r")

    game = GameState(board)

    moves = game.generate_legal_moves(GameState.WHITE)

    move_strings = {str(move) for move in moves}

    assert "a7b8Q" in move_strings
    assert "a7b8R" in move_strings
    assert "a7b8B" in move_strings
    assert "a7b8N" in move_strings


def test_invalid_promotion_piece_raises_error():
    board = empty_board()

    board.set_piece(7, 4, "K")
    board.set_piece(0, 4, "k")
    board.set_piece(1, 0, "P")

    game = GameState(board)

    with pytest.raises(ValueError):
        game.make_move(
            Move("a7", "a8", promotion="X")
        )


def test_undo_restores_promoted_pawn():
    board = empty_board()

    board.set_piece(7, 4, "K")
    board.set_piece(0, 4, "k")
    board.set_piece(1, 0, "P")

    game = GameState(board)

    game.make_move(
        Move("a7", "a8", promotion="Q")
    )

    assert game.board.get_piece(0, 0) == "Q"

    game.undo_move()

    assert game.board.get_piece(1, 0) == "P"
    assert game.board.get_piece(0, 0) == Board.EMPTY

def test_from_fen_initial_position():
    fen = (
        "rnbqkbnr/pppppppp/8/8/"
        "8/8/PPPPPPPP/RNBQKBNR "
        "w KQkq - 0 1"
    )

    game = GameState.from_fen(fen)

    assert game.side_to_move == GameState.WHITE
    assert game.castling_rights == {
        "K": True,
        "Q": True,
        "k": True,
        "q": True,
    }
    assert game.en_passant_target is None
    assert game.halfmove_clock == 0
    assert game.fullmove_number == 1

def test_cannot_capture_king():
    board = Board()

    for row in range(8):
        for column in range(8):
            board.set_piece(row, column, Board.EMPTY)

    board.set_piece(7, 4, "K")
    board.set_piece(0, 4, "k")
    board.set_piece(1, 4, "R")

    game = GameState(board=board)
    game.side_to_move = GameState.WHITE

    with pytest.raises(ValueError, match="Cannot capture the king"):
        game.make_move(Move("e7", "e8"))