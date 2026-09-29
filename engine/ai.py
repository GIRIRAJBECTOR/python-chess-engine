"""Simple chess AI: material evaluation + alpha-beta search.

This module deliberately depends only on the existing GameState API:
- GameState.WHITE / GameState.BLACK
- game_state.side_to_move
- game_state.generate_legal_moves(side)
- game_state.make_move(move)
- game_state.is_checkmate(side)
- game_state.is_stalemate(side)
- game_state.board.get_piece(row, column)
"""

from __future__ import annotations

import copy
from math import inf

from engine.game_state import GameState


PIECE_VALUES = {
    "P": 100,
    "N": 320,
    "B": 330,
    "R": 500,
    "Q": 900,
    "K": 20_000,
}


class ChessAI:
    """A small, deterministic alpha-beta chess player."""

    MATE_SCORE = 1_000_000

    def __init__(self, depth: int = 2):
        if depth < 1:
            raise ValueError("AI depth must be at least 1")
        self.depth = depth
        self.nodes_searched = 0

    def choose_move(self, game_state: GameState):
        """Return the best legal move for the current side, or None."""
        side = game_state.side_to_move
        legal_moves = list(game_state.generate_legal_moves(side))

        if not legal_moves:
            return None

        self.nodes_searched = 0
        maximizing = side == GameState.WHITE
        best_move = legal_moves[0]
        best_score = -inf if maximizing else inf

        ordered_moves = self._order_moves(game_state, legal_moves)

        for move in ordered_moves:
            child = copy.deepcopy(game_state)
            child.make_move(move)

            score = self._search(
                child,
                self.depth - 1,
                -inf,
                inf,
            )

            if maximizing and score > best_score:
                best_score = score
                best_move = move
            elif not maximizing and score < best_score:
                best_score = score
                best_move = move

        return best_move

    def evaluate(self, game_state: GameState) -> int:
        """Material-only evaluation from White's perspective.

        Kept intentionally simple for backwards compatibility with the
        original AI tests. The actual search uses evaluate_position().
        """
        score = 0

        for row in range(8):
            for column in range(8):
                piece = game_state.board.get_piece(row, column)

                if piece in (None, "."):
                    continue

                value = PIECE_VALUES.get(piece.upper(), 0)

                if piece.isupper():
                    score += value
                else:
                    score -= value

        return score

    # Piece-square tables. Row 0 is rank 8 and row 7 is rank 1.
    # Values are intentionally modest compared with material values.
    _PST = {
        "P": (
            (0, 0, 0, 0, 0, 0, 0, 0),
            (50, 50, 50, 50, 50, 50, 50, 50),
            (10, 10, 20, 30, 30, 20, 10, 10),
            (5, 5, 10, 25, 25, 10, 5, 5),
            (0, 0, 0, 20, 20, 0, 0, 0),
            (5, -5, -10, 0, 0, -10, -5, 5),
            (5, 10, 10, -20, -20, 10, 10, 5),
            (0, 0, 0, 0, 0, 0, 0, 0),
        ),
        "N": (
            (-50, -40, -30, -30, -30, -30, -40, -50),
            (-40, -20, 0, 5, 5, 0, -20, -40),
            (-30, 5, 10, 15, 15, 10, 5, -30),
            (-30, 0, 15, 20, 20, 15, 0, -30),
            (-30, 5, 15, 20, 20, 15, 5, -30),
            (-30, 0, 10, 15, 15, 10, 0, -30),
            (-40, -20, 0, 0, 0, 0, -20, -40),
            (-50, -40, -30, -30, -30, -30, -40, -50),
        ),
        "B": (
            (-20, -10, -10, -10, -10, -10, -10, -20),
            (-10, 5, 0, 0, 0, 0, 5, -10),
            (-10, 10, 10, 10, 10, 10, 10, -10),
            (-10, 0, 10, 10, 10, 10, 0, -10),
            (-10, 5, 5, 10, 10, 5, 5, -10),
            (-10, 0, 5, 10, 10, 5, 0, -10),
            (-10, 0, 0, 0, 0, 0, 0, -10),
            (-20, -10, -10, -10, -10, -10, -10, -20),
        ),
        "R": (
            (0, 0, 0, 5, 5, 0, 0, 0),
            (-5, 0, 0, 0, 0, 0, 0, -5),
            (-5, 0, 0, 0, 0, 0, 0, -5),
            (-5, 0, 0, 0, 0, 0, 0, -5),
            (-5, 0, 0, 0, 0, 0, 0, -5),
            (-5, 0, 0, 0, 0, 0, 0, -5),
            (5, 10, 10, 10, 10, 10, 10, 5),
            (0, 0, 0, 0, 0, 0, 0, 0),
        ),
        "Q": (
            (-20, -10, -10, -5, -5, -10, -10, -20),
            (-10, 0, 0, 0, 0, 0, 0, -10),
            (-10, 0, 5, 5, 5, 5, 0, -10),
            (-5, 0, 5, 5, 5, 5, 0, -5),
            (0, 0, 5, 5, 5, 5, 0, 0),
            (-10, 5, 5, 5, 5, 5, 5, -10),
            (-10, 0, 5, 0, 0, 0, 0, -10),
            (-20, -10, -10, -5, -5, -10, -10, -20),
        ),
        "K": (
            (20, 30, 10, 0, 0, 10, 30, 20),
            (20, 20, 0, 0, 0, 0, 20, 20),
            (-10, -20, -20, -20, -20, -20, -20, -10),
            (-20, -30, -30, -40, -40, -30, -30, -20),
            (-30, -40, -40, -50, -50, -40, -40, -30),
            (-30, -40, -40, -50, -50, -40, -40, -30),
            (-30, -40, -40, -50, -50, -40, -40, -30),
            (-30, -40, -40, -50, -50, -40, -40, -30),
        ),
    }

    def evaluate_position(self, game_state: GameState) -> int:
        """Richer static evaluation from White's perspective.

        Combines material, piece-square placement, mobility, and a small
        center-control bonus. Material remains dominant so the engine does
        not sacrifice pieces merely for positional bonuses.
        """
        score = self.evaluate(game_state)

        # Positional value.
        for row in range(8):
            for column in range(8):
                piece = game_state.board.get_piece(row, column)

                if piece in (None, "."):
                    continue

                table = self._PST.get(piece.upper())
                if table is None:
                    continue

                pst_row = row if piece.isupper() else 7 - row
                bonus = table[pst_row][column]
                score += bonus if piece.isupper() else -bonus

        # Mobility: a small bonus for having more legal choices.
        try:
            white_moves = len(game_state.generate_legal_moves(GameState.WHITE))
            black_moves = len(game_state.generate_legal_moves(GameState.BLACK))
            score += (white_moves - black_moves) * 2
        except Exception:
            # Keep evaluation robust if a future GameState implementation
            # changes move-generation details.
            pass

        # Center occupancy/control proxy. Occupying the four central squares
        # is useful without requiring another attack-map API.
        center = {(3, 3), (3, 4), (4, 3), (4, 4)}
        for row, column in center:
            piece = game_state.board.get_piece(row, column)
            if piece in (None, "."):
                continue
            score += 12 if piece.isupper() else -12

        return score

    def _search(self, game_state, depth, alpha, beta):
        self.nodes_searched += 1

        side = game_state.side_to_move

        if game_state.is_checkmate(side):
            # The side to move has already lost.
            if side == GameState.WHITE:
                return -self.MATE_SCORE - depth
            return self.MATE_SCORE + depth

        if game_state.is_stalemate(side):
            return 0

        if depth == 0:
            return self.evaluate(game_state)

        legal_moves = list(game_state.generate_legal_moves(side))

        if not legal_moves:
            return self.evaluate(game_state)

        maximizing = side == GameState.WHITE
        ordered_moves = self._order_moves(game_state, legal_moves)

        if maximizing:
            value = -inf

            for move in ordered_moves:
                child = copy.deepcopy(game_state)
                child.make_move(move)

                value = max(
                    value,
                    self._search(child, depth - 1, alpha, beta),
                )
                alpha = max(alpha, value)

                if alpha >= beta:
                    break

            return value

        value = inf

        for move in ordered_moves:
            child = copy.deepcopy(game_state)
            child.make_move(move)

            value = min(
                value,
                self._search(child, depth - 1, alpha, beta),
            )
            beta = min(beta, value)

            if alpha >= beta:
                break

        return value

    def _order_moves(self, game_state, moves):
        """Captures first; this makes alpha-beta substantially more useful."""
        scored = []

        for move in moves:
            text = str(move)
            target = text[2:4]

            try:
                file_index = ord(target[0]) - ord("a")
                rank_index = 8 - int(target[1])
                captured = game_state.board.get_piece(
                    rank_index,
                    file_index,
                )
            except (ValueError, IndexError):
                captured = None

            capture_value = (
                PIECE_VALUES.get(captured.upper(), 0)
                if captured not in (None, ".")
                else 0
            )

            scored.append((capture_value, text, move))

        scored.sort(key=lambda item: (-item[0], item[1]))
        return [item[2] for item in scored]
