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
        """Static evaluation from White's perspective."""
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
