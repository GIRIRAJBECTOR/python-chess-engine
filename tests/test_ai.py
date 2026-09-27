from engine.game_state import GameState
from engine.ai import ChessAI


def test_ai_returns_a_legal_move_from_start_position():
    game = GameState()
    ai = ChessAI(depth=1)

    move = ai.choose_move(game)

    assert move is not None
    legal = {str(candidate) for candidate in game.generate_legal_moves(game.side_to_move)}
    assert str(move) in legal


def test_ai_depth_validation():
    try:
        ChessAI(depth=0)
        assert False, "Expected ValueError"
    except ValueError:
        pass


def test_ai_material_evaluation():
    game = GameState.from_fen(
        "8/8/8/8/8/8/4Q3/4K2k w - - 0 1"
    )
    ai = ChessAI(depth=1)

    assert ai.evaluate(game) > 0


def test_ai_handles_game_over_position():
    game = GameState.from_fen(
        "7k/6Q1/5K2/8/8/8/8/8 b - - 0 1"
    )
    ai = ChessAI(depth=1)

    # This position is checkmate: Black has no legal move.
    assert game.is_checkmate(GameState.BLACK)
    assert ai.choose_move(game) is None
