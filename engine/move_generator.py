from engine.coordinates import (
    square_to_position,
    position_to_square,
)
from engine.move import Move


class MoveGenerator:

    @staticmethod
    def is_white(piece):
        return piece.isupper()

    @staticmethod
    def is_black(piece):
        return piece.islower()

    @staticmethod
    def is_opponent(piece, moving_piece):
        """
        Check whether a piece belongs to the opponent.
        """

        if piece == ".":
            return False

        if MoveGenerator.is_white(moving_piece):
            return MoveGenerator.is_black(piece)

        return MoveGenerator.is_white(piece)

    # ==========================================================
    # PAWN
    # ==========================================================

    @staticmethod
    def generate_pawn_moves(board, square):
        """
        Generate pseudo-legal pawn moves.

        Currently supports:
        - One-square movement
        - Two-square initial movement
        - Diagonal captures

        Not yet implemented:
        - Promotion
        - En-passant
        - King safety
        """

        row, column = square_to_position(square)
        pawn = board.get_piece(row, column)

        if pawn not in ("P", "p"):
            raise ValueError(
                f"{square} does not contain a pawn"
            )

        moves = []

        if pawn == "P":
            direction = -1
            starting_row = 6
        else:
            direction = 1
            starting_row = 1

        # ------------------------------------------------------
        # One-square forward move
        # ------------------------------------------------------

        next_row = row + direction

        if 0 <= next_row < 8:

            if board.get_piece(next_row, column) == ".":
                moves.append(
                    Move(
                        square,
                        position_to_square(
                            next_row,
                            column
                        )
                    )
                )

                # --------------------------------------------------
                # Two-square initial move
                # --------------------------------------------------

                if row == starting_row:

                    double_row = row + (2 * direction)

                    if board.get_piece(
                        double_row,
                        column
                    ) == ".":
                        moves.append(
                            Move(
                                square,
                                position_to_square(
                                    double_row,
                                    column
                                )
                            )
                        )

        # ------------------------------------------------------
        # Diagonal captures
        # ------------------------------------------------------

        for column_offset in (-1, 1):

            capture_column = column + column_offset

            if not (0 <= next_row < 8):
                continue

            if not (0 <= capture_column < 8):
                continue

            target = board.get_piece(
                next_row,
                capture_column
            )

            if MoveGenerator.is_opponent(
                target,
                pawn
            ):
                moves.append(
                    Move(
                        square,
                        position_to_square(
                            next_row,
                            capture_column
                        )
                    )
                )

        return moves

    # ==========================================================
    # KNIGHT
    # ==========================================================

    @staticmethod
    def generate_knight_moves(board, square):
        """
        Generate pseudo-legal knight moves.

        Knights move:
        - 2 rows + 1 column
        - 1 row + 2 columns

        Knights can jump over other pieces.
        """

        row, column = square_to_position(square)
        knight = board.get_piece(row, column)

        if knight not in ("N", "n"):
            raise ValueError(
                f"{square} does not contain a knight"
            )

        moves = []

        offsets = [
            (-2, -1),
            (-2, 1),
            (-1, -2),
            (-1, 2),
            (1, -2),
            (1, 2),
            (2, -1),
            (2, 1),
        ]

        for row_offset, column_offset in offsets:

            target_row = row + row_offset
            target_column = column + column_offset

            # Outside board.
            if not (0 <= target_row < 8):
                continue

            if not (0 <= target_column < 8):
                continue

            target = board.get_piece(
                target_row,
                target_column
            )

            # Empty square.
            if target == ".":
                moves.append(
                    Move(
                        square,
                        position_to_square(
                            target_row,
                            target_column
                        )
                    )
                )

            # Capture opponent piece.
            elif MoveGenerator.is_opponent(
                target,
                knight
            ):
                moves.append(
                    Move(
                        square,
                        position_to_square(
                            target_row,
                            target_column
                        )
                    )
                )

        return moves