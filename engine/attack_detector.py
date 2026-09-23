from engine.coordinates import square_to_position


class AttackDetector:
    KNIGHT_OFFSETS = [
        (-2, -1),
        (-2, 1),
        (-1, -2),
        (-1, 2),
        (1, -2),
        (1, 2),
        (2, -1),
        (2, 1),
    ]

    KING_OFFSETS = [
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (0, -1),
        (0, 1),
        (1, -1),
        (1, 0),
        (1, 1),
    ]

    BISHOP_DIRECTIONS = [
        (-1, -1),
        (-1, 1),
        (1, -1),
        (1, 1),
    ]

    ROOK_DIRECTIONS = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1),
    ]

    @staticmethod
    def is_square_attacked(board, square, by_color):
        row, column = square_to_position(square)

        if by_color not in ("white", "black"):
            raise ValueError(f"Invalid color: {by_color}")

        if AttackDetector._pawn_attacks(
            board, row, column, by_color
        ):
            return True

        if AttackDetector._knight_attacks(
            board, row, column, by_color
        ):
            return True

        if AttackDetector._king_attacks(
            board, row, column, by_color
        ):
            return True

        if AttackDetector._sliding_attacks(
            board,
            row,
            column,
            by_color,
            AttackDetector.BISHOP_DIRECTIONS,
            ("B", "Q") if by_color == "white" else ("b", "q"),
        ):
            return True

        if AttackDetector._sliding_attacks(
            board,
            row,
            column,
            by_color,
            AttackDetector.ROOK_DIRECTIONS,
            ("R", "Q") if by_color == "white" else ("r", "q"),
        ):
            return True

        return False

    @staticmethod
    def _pawn_attacks(board, row, column, by_color):
        # We look backwards from the target square to find
        # pawns that could attack it.
        if by_color == "white":
            pawn_row = row + 1
            pawn = "P"
        else:
            pawn_row = row - 1
            pawn = "p"

        if not 0 <= pawn_row < 8:
            return False

        for column_offset in (-1, 1):
            pawn_column = column + column_offset

            if not 0 <= pawn_column < 8:
                continue

            if board.get_piece(pawn_row, pawn_column) == pawn:
                return True

        return False

    @staticmethod
    def _knight_attacks(board, row, column, by_color):
        knight = "N" if by_color == "white" else "n"

        for row_offset, column_offset in AttackDetector.KNIGHT_OFFSETS:
            attacker_row = row + row_offset
            attacker_column = column + column_offset

            if not (
                0 <= attacker_row < 8
                and 0 <= attacker_column < 8
            ):
                continue

            if board.get_piece(
                attacker_row,
                attacker_column,
            ) == knight:
                return True

        return False

    @staticmethod
    def _king_attacks(board, row, column, by_color):
        king = "K" if by_color == "white" else "k"

        for row_offset, column_offset in AttackDetector.KING_OFFSETS:
            attacker_row = row + row_offset
            attacker_column = column + column_offset

            if not (
                0 <= attacker_row < 8
                and 0 <= attacker_column < 8
            ):
                continue

            if board.get_piece(
                attacker_row,
                attacker_column,
            ) == king:
                return True

        return False

    @staticmethod
    def _sliding_attacks(
        board,
        row,
        column,
        by_color,
        directions,
        attackers,
    ):
        for row_direction, column_direction in directions:
            attacker_row = row + row_direction
            attacker_column = column + column_direction

            while (
                0 <= attacker_row < 8
                and 0 <= attacker_column < 8
            ):
                piece = board.get_piece(
                    attacker_row,
                    attacker_column,
                )

                if piece != ".":
                    if piece in attackers:
                        return True

                    # Any piece blocks the ray.
                    break

                attacker_row += row_direction
                attacker_column += column_direction

        return False