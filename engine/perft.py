from engine.game_state import GameState


def perft(game, depth):
    """
    Count all legal move sequences from the current position
    up to the requested depth.
    """

    if depth < 0:
        raise ValueError("Depth cannot be negative")

    if depth == 0:
        return 1

    total_nodes = 0

    legal_moves = game.generate_legal_moves()

    for move in legal_moves:
        game.make_move(move)

        total_nodes += perft(
            game,
            depth - 1,
        )

        game.undo_move()

    return total_nodes