from engine.game_state import GameState
from engine.perft import perft


def test_perft_depth_zero():
    game = GameState()

    assert perft(game, 0) == 1


def test_initial_position_perft_depth_one():
    game = GameState()

    assert perft(game, 1) == 20


def test_initial_position_perft_depth_two():
    game = GameState()

    assert perft(game, 2) == 400


def test_initial_position_perft_depth_three():
    game = GameState()

    assert perft(game, 3) == 8902


def test_perft_does_not_change_game_state():
    game = GameState()

    original_board = [row[:] for row in game.board.board]
    original_side = game.side_to_move
    original_castling_rights = game.castling_rights.copy()
    original_en_passant = game.en_passant_target
    original_halfmove = game.halfmove_clock
    original_fullmove = game.fullmove_number
    original_history = game.move_history[:]

    perft(game, 3)

    assert game.board.board == original_board
    assert game.side_to_move == original_side
    assert game.castling_rights == original_castling_rights
    assert game.en_passant_target == original_en_passant
    assert game.halfmove_clock == original_halfmove
    assert game.fullmove_number == original_fullmove
    assert game.move_history == original_history


def test_perft_position_with_castling():
    game = GameState()

    for square in ("b1", "c1", "d1", "f1", "g1"):
        row = 8 - int(square[1])
        column = ord(square[0]) - ord("a")
        game.board.set_piece(row, column, ".")

    moves = game.generate_legal_moves()

    move_strings = [str(move) for move in moves]

    assert "e1g1" in move_strings
    assert "e1c1" in move_strings


def test_perft_position_with_en_passant():
    game = GameState()

    for row in range(8):
        for column in range(8):
            game.board.set_piece(row, column, ".")

    game.board.set_piece(7, 4, "K")
    game.board.set_piece(0, 4, "k")

    game.board.set_piece(3, 4, "P")
    game.board.set_piece(3, 3, "p")

    game.side_to_move = GameState.WHITE
    game.en_passant_target = "d6"

    moves = game.generate_legal_moves()

    assert "e5d6" in [str(move) for move in moves]


def test_perft_position_with_promotion():
    game = GameState()

    for row in range(8):
        for column in range(8):
            game.board.set_piece(row, column, ".")

    game.board.set_piece(7, 4, "K")
    game.board.set_piece(0, 4, "k")
    game.board.set_piece(1, 0, "P")

    game.side_to_move = GameState.WHITE

    moves = game.generate_legal_moves()

    promotion_moves = [
        str(move)
        for move in moves
        if str(move).startswith("a7a8")
    ]

    assert sorted(promotion_moves) == [
        "a7a8B",
        "a7a8N",
        "a7a8Q",
        "a7a8R",
    ]


def test_standard_perft_position_two_depth_one():
    fen = (
        "r3k2r/p1ppqpb1/bn2pnp1/3PN3/"
    "1p2P3/2N2Q1p/PPPBBPPP/R3K2R "
    "w KQkq - 0 1"
    )

    game = GameState.from_fen(fen)

    assert perft(game, 1) == 48


def test_standard_perft_position_two_depth_two():
    fen = (
        "r3k2r/p1ppqpb1/bn2pnp1/3PN3/"
    "1p2P3/2N2Q1p/PPPBBPPP/R3K2R "
    "w KQkq - 0 1"
    )

    game = GameState.from_fen(fen)

    assert perft(game, 2) == 2039


def test_standard_perft_position_two_depth_three():
    fen = (
        "r3k2r/p1ppqpb1/bn2pnp1/3PN3/"
    "1p2P3/2N2Q1p/PPPBBPPP/R3K2R "
    "w KQkq - 0 1"
    )

    game = GameState.from_fen(fen)

    assert perft(game, 3) == 97862


def test_standard_perft_position_two_depth_four():
    fen = (
        "r3k2r/p1ppqpb1/bn2pnp1/3PN3/"
    "1p2P3/2N2Q1p/PPPBBPPP/R3K2R "
    "w KQkq - 0 1"
    )

    game = GameState.from_fen(fen)

    assert perft(game, 4) == 4085603


def test_standard_perft_position_three_depth_one():
    fen = (
        "8/2p5/3p4/KP5r/"
        "1R3p1k/8/4P1P1/8 "
        "w - - 0 1"
    )

    game = GameState.from_fen(fen)

    assert perft(game, 1) == 14


def test_standard_perft_position_three_depth_two():
    fen = (
        "8/2p5/3p4/KP5r/"
        "1R3p1k/8/4P1P1/8 "
        "w - - 0 1"
    )

    game = GameState.from_fen(fen)

    assert perft(game, 2) == 191


def test_standard_perft_position_three_depth_three():
    fen = (
        "8/2p5/3p4/KP5r/"
        "1R3p1k/8/4P1P1/8 "
        "w - - 0 1"
    )

    game = GameState.from_fen(fen)

    assert perft(game, 3) == 2812