from copy import deepcopy

from engine.attack_detector import AttackDetector
from engine.board import Board
from engine.coordinates import position_to_square, square_to_position
from engine.move import Move
from engine.move_generator import MoveGenerator


class GameState:
    WHITE = "white"
    BLACK = "black"

    def __init__(self, board=None):
        self.board = board if board is not None else Board()

        self.side_to_move = self.WHITE

        self.castling_rights = {
            "K": True,
            "Q": True,
            "k": True,
            "q": True,
        }

        self.en_passant_target = None

        self.halfmove_clock = 0
        self.fullmove_number = 1

        self.move_history = []

        self._undo_stack = []

    @classmethod
    def from_fen(cls, fen):
        parts = fen.split()

        if len(parts) != 6:
            raise ValueError("Invalid FEN")

        (
            board_part,
            side_part,
            castling_part,
            ep_part,
            halfmove_part,
            fullmove_part,
        ) = parts

        ranks = board_part.split("/")

        if len(ranks) != 8:
            raise ValueError("Invalid FEN board")

        board = Board()

        # Clear the board before loading the FEN position.
        for row in range(8):
            for column in range(8):
                board.set_piece(row, column, Board.EMPTY)

        for row in range(8):
            column = 0

            for char in ranks[row]:
                if char.isdigit():
                    empty_squares = int(char)

                    if empty_squares < 1 or empty_squares > 8:
                        raise ValueError("Invalid FEN empty-square count")

                    column += empty_squares

                else:
                    if char not in "PNBRQKpnbrqk":
                        raise ValueError(
                            f"Invalid FEN piece: {char}"
                        )

                    if column >= 8:
                        raise ValueError("Invalid FEN rank")

                    board.set_piece(
                        row,
                        column,
                        char,
                    )

                    column += 1

            if column != 8:
                raise ValueError("Invalid FEN rank")

        if side_part == "w":
            side_to_move = cls.WHITE

        elif side_part == "b":
            side_to_move = cls.BLACK

        else:
            raise ValueError("Invalid FEN side")

        valid_castling_characters = set("KQkq")

        if castling_part != "-":
            if any(
                character not in valid_castling_characters
                for character in castling_part
            ):
                raise ValueError("Invalid FEN castling rights")

            if len(set(castling_part)) != len(castling_part):
                raise ValueError("Invalid FEN castling rights")

        castling_rights = {
            "K": "K" in castling_part,
            "Q": "Q" in castling_part,
            "k": "k" in castling_part,
            "q": "q" in castling_part,
        }

        if ep_part == "-":
            en_passant_target = None
        else:
            # Validate the en-passant square.
            square_to_position(ep_part)
            en_passant_target = ep_part

        try:
            halfmove_clock = int(halfmove_part)
            fullmove_number = int(fullmove_part)
        except ValueError as exc:
            raise ValueError(
                "Invalid FEN move counters"
            ) from exc

        if halfmove_clock < 0:
            raise ValueError("Invalid FEN halfmove clock")

        if fullmove_number < 1:
            raise ValueError("Invalid FEN fullmove number")

        game = cls(board=board)

        game.side_to_move = side_to_move
        game.castling_rights = castling_rights
        game.en_passant_target = en_passant_target
        game.halfmove_clock = halfmove_clock
        game.fullmove_number = fullmove_number

        return game

    def switch_side(self):
        if self.side_to_move == self.WHITE:
            self.side_to_move = self.BLACK
        else:
            self.side_to_move = self.WHITE

    def can_castle_kingside(self, color):
        if color == self.WHITE:
            return self.castling_rights["K"]

        if color == self.BLACK:
            return self.castling_rights["k"]

        raise ValueError(f"Invalid color: {color}")

    def can_castle_queenside(self, color):
        if color == self.WHITE:
            return self.castling_rights["Q"]

        if color == self.BLACK:
            return self.castling_rights["q"]

        raise ValueError(f"Invalid color: {color}")

    def reset_en_passant(self):
        self.en_passant_target = None

    def _snapshot(self):
        return {
            "board": deepcopy(self.board.board),
            "side_to_move": self.side_to_move,
            "castling_rights": self.castling_rights.copy(),
            "en_passant_target": self.en_passant_target,
            "halfmove_clock": self.halfmove_clock,
            "fullmove_number": self.fullmove_number,
        }

    def _restore_snapshot(self, snapshot):
        self.board.board = deepcopy(snapshot["board"])
        self.side_to_move = snapshot["side_to_move"]
        self.castling_rights = snapshot["castling_rights"].copy()
        self.en_passant_target = snapshot["en_passant_target"]
        self.halfmove_clock = snapshot["halfmove_clock"]
        self.fullmove_number = snapshot["fullmove_number"]

    def _find_king(self, color):
        king = "K" if color == self.WHITE else "k"

        for row in range(8):
            for column in range(8):
                if self.board.get_piece(row, column) == king:
                    return position_to_square(row, column)

        raise ValueError(f"{color} king not found")

    def is_in_check(self, color):
        if color not in (self.WHITE, self.BLACK):
            raise ValueError(f"Invalid color: {color}")

        king_square = self._find_king(color)

        attacking_color = (
            self.BLACK
            if color == self.WHITE
            else self.WHITE
        )

        return AttackDetector.is_square_attacked(
            self.board,
            king_square,
            attacking_color,
        )

    def is_checkmate(self, color=None):
        if color is None:
            color = self.side_to_move

        if color not in (self.WHITE, self.BLACK):
            raise ValueError(f"Invalid color: {color}")

        if not self.is_in_check(color):
            return False

        return len(self.generate_legal_moves(color)) == 0

    def is_stalemate(self, color=None):
        if color is None:
            color = self.side_to_move

        if color not in (self.WHITE, self.BLACK):
            raise ValueError(f"Invalid color: {color}")

        if self.is_in_check(color):
            return False

        return len(self.generate_legal_moves(color)) == 0

    def is_game_over(self):
        return (
            self.is_checkmate(self.side_to_move)
            or self.is_stalemate(self.side_to_move)
        )

    def _generate_castling_moves(self, color):
        moves = []

        if color == self.WHITE:
            if self.board.get_piece(7, 4) != "K":
                return moves

            if self.castling_rights["K"]:
                if (
                    self.board.get_piece(7, 5) == Board.EMPTY
                    and self.board.get_piece(7, 6) == Board.EMPTY
                    and self.board.get_piece(7, 7) == "R"
                ):
                    if (
                        not self.is_in_check(self.WHITE)
                        and not AttackDetector.is_square_attacked(
                            self.board,
                            "f1",
                            self.BLACK,
                        )
                        and not AttackDetector.is_square_attacked(
                            self.board,
                            "g1",
                            self.BLACK,
                        )
                    ):
                        moves.append(Move("e1", "g1"))

            if self.castling_rights["Q"]:
                if (
                    self.board.get_piece(7, 1) == Board.EMPTY
                    and self.board.get_piece(7, 2) == Board.EMPTY
                    and self.board.get_piece(7, 3) == Board.EMPTY
                    and self.board.get_piece(7, 0) == "R"
                ):
                    if (
                        not self.is_in_check(self.WHITE)
                        and not AttackDetector.is_square_attacked(
                            self.board,
                            "d1",
                            self.BLACK,
                        )
                        and not AttackDetector.is_square_attacked(
                            self.board,
                            "c1",
                            self.BLACK,
                        )
                    ):
                        moves.append(Move("e1", "c1"))

        else:
            if self.board.get_piece(0, 4) != "k":
                return moves

            if self.castling_rights["k"]:
                if (
                    self.board.get_piece(0, 5) == Board.EMPTY
                    and self.board.get_piece(0, 6) == Board.EMPTY
                    and self.board.get_piece(0, 7) == "r"
                ):
                    if (
                        not self.is_in_check(self.BLACK)
                        and not AttackDetector.is_square_attacked(
                            self.board,
                            "f8",
                            self.WHITE,
                        )
                        and not AttackDetector.is_square_attacked(
                            self.board,
                            "g8",
                            self.WHITE,
                        )
                    ):
                        moves.append(Move("e8", "g8"))

            if self.castling_rights["q"]:
                if (
                    self.board.get_piece(0, 1) == Board.EMPTY
                    and self.board.get_piece(0, 2) == Board.EMPTY
                    and self.board.get_piece(0, 3) == Board.EMPTY
                    and self.board.get_piece(0, 0) == "r"
                ):
                    if (
                        not self.is_in_check(self.BLACK)
                        and not AttackDetector.is_square_attacked(
                            self.board,
                            "d8",
                            self.WHITE,
                        )
                        and not AttackDetector.is_square_attacked(
                            self.board,
                            "c8",
                            self.WHITE,
                        )
                    ):
                        moves.append(Move("e8", "c8"))

        return moves

    def _generate_en_passant_moves(self, color):
        moves = []

        if self.en_passant_target is None:
            return moves

        target_row, target_column = square_to_position(
            self.en_passant_target
        )

        if color == self.WHITE:
            pawn = "P"
            pawn_row = target_row + 1

            if pawn_row != 3:
                return moves

            for source_column in (
                target_column - 1,
                target_column + 1,
            ):
                if not 0 <= source_column < 8:
                    continue

                if self.board.get_piece(
                    pawn_row,
                    source_column,
                ) == pawn:
                    moves.append(
                        Move(
                            position_to_square(
                                pawn_row,
                                source_column,
                            ),
                            self.en_passant_target,
                        )
                    )

        else:
            pawn = "p"
            pawn_row = target_row - 1

            if pawn_row != 4:
                return moves

            for source_column in (
                target_column - 1,
                target_column + 1,
            ):
                if not 0 <= source_column < 8:
                    continue

                if self.board.get_piece(
                    pawn_row,
                    source_column,
                ) == pawn:
                    moves.append(
                        Move(
                            position_to_square(
                                pawn_row,
                                source_column,
                            ),
                            self.en_passant_target,
                        )
                    )

        return moves

    def _expand_promotion_moves(self, moves):
        expanded_moves = []

        for move in moves:
            to_row, _ = square_to_position(move.to_square)

            if to_row in (0, 7):
                from_row, from_column = square_to_position(
                    move.from_square
                )

                piece = self.board.get_piece(
                    from_row,
                    from_column,
                )

                if piece.lower() == "p":
                    if piece.isupper():
                        promotions = ("Q", "R", "B", "N")
                    else:
                        promotions = ("q", "r", "b", "n")

                    for promotion in promotions:
                        expanded_moves.append(
                            Move(
                                move.from_square,
                                move.to_square,
                                promotion=promotion,
                            )
                        )

                    continue

            expanded_moves.append(move)

        return expanded_moves

    def generate_pseudo_legal_moves(self, color=None):
        if color is None:
            color = self.side_to_move

        if color not in (self.WHITE, self.BLACK):
            raise ValueError(f"Invalid color: {color}")

        moves = []

        for row in range(8):
            for column in range(8):
                piece = self.board.get_piece(row, column)

                if piece == Board.EMPTY:
                    continue

                if color == self.WHITE and not piece.isupper():
                    continue

                if color == self.BLACK and not piece.islower():
                    continue

                square = position_to_square(row, column)

                if piece.lower() == "p":
                    piece_moves = MoveGenerator.generate_pawn_moves(
                        self.board,
                        square,
                    )

                elif piece.lower() == "n":
                    piece_moves = MoveGenerator.generate_knight_moves(
                        self.board,
                        square,
                    )

                elif piece.lower() == "b":
                    piece_moves = MoveGenerator.generate_bishop_moves(
                        self.board,
                        square,
                    )

                elif piece.lower() == "r":
                    piece_moves = MoveGenerator.generate_rook_moves(
                        self.board,
                        square,
                    )

                elif piece.lower() == "q":
                    piece_moves = MoveGenerator.generate_queen_moves(
                        self.board,
                        square,
                    )

                elif piece.lower() == "k":
                    piece_moves = MoveGenerator.generate_king_moves(
                        self.board,
                        square,
                    )

                else:
                    continue

                moves.extend(piece_moves)

        moves.extend(self._generate_castling_moves(color))
        moves.extend(self._generate_en_passant_moves(color))

        return self._expand_promotion_moves(moves)

    def generate_legal_moves(self, color=None):
        if color is None:
            color = self.side_to_move

        if color not in (self.WHITE, self.BLACK):
            raise ValueError(f"Invalid color: {color}")

        original_side = self.side_to_move

        self.side_to_move = color

        legal_moves = []

        pseudo_legal_moves = self.generate_pseudo_legal_moves(color)

        for move in pseudo_legal_moves:
            try:
                self.make_move(move)

                if not self.is_in_check(color):
                    legal_moves.append(move)

                self.undo_move()

            except (ValueError, TypeError):
                if self._undo_stack:
                    self.undo_move()

        self.side_to_move = original_side

        return legal_moves

    def _update_castling_rights_after_move(
        self,
        moving_piece,
        from_square,
        to_square,
        captured_piece,
    ):
        if moving_piece == "K":
            self.castling_rights["K"] = False
            self.castling_rights["Q"] = False

        elif moving_piece == "k":
            self.castling_rights["k"] = False
            self.castling_rights["q"] = False

        elif moving_piece == "R":
            if from_square == "a1":
                self.castling_rights["Q"] = False
            elif from_square == "h1":
                self.castling_rights["K"] = False

        elif moving_piece == "r":
            if from_square == "a8":
                self.castling_rights["q"] = False
            elif from_square == "h8":
                self.castling_rights["k"] = False

        if captured_piece == "R":
            if to_square == "a1":
                self.castling_rights["Q"] = False
            elif to_square == "h1":
                self.castling_rights["K"] = False

        elif captured_piece == "r":
            if to_square == "a8":
                self.castling_rights["q"] = False
            elif to_square == "h8":
                self.castling_rights["k"] = False

    def _is_castling_move(self, move):
        return move in (
            Move("e1", "g1"),
            Move("e1", "c1"),
            Move("e8", "g8"),
            Move("e8", "c8"),
        )

    def _is_en_passant_move(self, move, moving_piece):
        if moving_piece.lower() != "p":
            return False

        if self.en_passant_target is None:
            return False

        if move.to_square != self.en_passant_target:
            return False

        from_row, from_column = square_to_position(
            move.from_square
        )

        to_row, to_column = square_to_position(
            move.to_square
        )

        if abs(from_column - to_column) != 1:
            return False

        if moving_piece == "P":
            return (
                from_row == 3
                and to_row == 2
                and self.board.get_piece(
                    to_row + 1,
                    to_column,
                ) == "p"
            )

        return (
            from_row == 4
            and to_row == 5
            and self.board.get_piece(
                to_row - 1,
                to_column,
            ) == "P"
        )

    def _make_castling_move(self, move):
        if move == Move("e1", "g1"):
            self.board.set_piece(7, 4, Board.EMPTY)
            self.board.set_piece(7, 6, "K")

            self.board.set_piece(7, 7, Board.EMPTY)
            self.board.set_piece(7, 5, "R")

            self.castling_rights["K"] = False
            self.castling_rights["Q"] = False

        elif move == Move("e1", "c1"):
            self.board.set_piece(7, 4, Board.EMPTY)
            self.board.set_piece(7, 2, "K")

            self.board.set_piece(7, 0, Board.EMPTY)
            self.board.set_piece(7, 3, "R")

            self.castling_rights["K"] = False
            self.castling_rights["Q"] = False

        elif move == Move("e8", "g8"):
            self.board.set_piece(0, 4, Board.EMPTY)
            self.board.set_piece(0, 6, "k")

            self.board.set_piece(0, 7, Board.EMPTY)
            self.board.set_piece(0, 5, "r")

            self.castling_rights["k"] = False
            self.castling_rights["q"] = False

        elif move == Move("e8", "c8"):
            self.board.set_piece(0, 4, Board.EMPTY)
            self.board.set_piece(0, 0, Board.EMPTY)
            self.board.set_piece(0, 2, "k")
            self.board.set_piece(0, 3, "r")

            self.castling_rights["k"] = False
            self.castling_rights["q"] = False

        else:
            raise ValueError("Invalid castling move")

    def make_move(self, move):
        if not isinstance(move, Move):
            raise TypeError("move must be a Move instance")

        from_row, from_column = square_to_position(
            move.from_square
        )

        to_row, to_column = square_to_position(
            move.to_square
        )

        moving_piece = self.board.get_piece(
            from_row,
            from_column,
        )

        captured_piece = self.board.get_piece(
            to_row,
            to_column,
        )

        if moving_piece == Board.EMPTY:
            raise ValueError(
                f"No piece on source square: {move.from_square}"
            )

        if self.side_to_move == self.WHITE:
            if not moving_piece.isupper():
                raise ValueError("It is White's turn")
        else:
            if not moving_piece.islower():
                raise ValueError("It is Black's turn")

        if move.promotion is not None:
            if moving_piece.lower() != "p":
                raise ValueError(
                    "Only pawns can be promoted"
                )

            valid_promotions = (
                {"Q", "R", "B", "N"}
                if moving_piece.isupper()
                else {"q", "r", "b", "n"}
            )

            if move.promotion not in valid_promotions:
                raise ValueError(
                    f"Invalid promotion piece: {move.promotion}"
                )

            if to_row not in (0, 7):
                raise ValueError(
                    "Pawn must reach the last rank to promote"
                )

        if captured_piece != Board.EMPTY:
            if captured_piece.lower() == "k":
                raise ValueError("Cannot capture the king")

            if (
                moving_piece.isupper()
                and captured_piece.isupper()
            ):
                raise ValueError(
                    "Cannot capture your own piece"
                )

            if (
                moving_piece.islower()
                and captured_piece.islower()
            ):
                raise ValueError(
                    "Cannot capture your own piece"
                )

        is_en_passant = self._is_en_passant_move(
            move,
            moving_piece,
        )

        if is_en_passant:
            captured_piece = (
                "p" if moving_piece == "P" else "P"
            )

        self._undo_stack.append(self._snapshot())
        self.move_history.append(move)

        if self._is_castling_move(move):
            self._make_castling_move(move)

        else:
            self.board.set_piece(
                from_row,
                from_column,
                Board.EMPTY,
            )

            placed_piece = moving_piece

            if move.promotion is not None:
                placed_piece = move.promotion

            self.board.set_piece(
                to_row,
                to_column,
                placed_piece,
            )

            if is_en_passant:
                if moving_piece == "P":
                    captured_pawn_row = to_row + 1
                else:
                    captured_pawn_row = to_row - 1

                self.board.set_piece(
                    captured_pawn_row,
                    to_column,
                    Board.EMPTY,
                )

            self._update_castling_rights_after_move(
                moving_piece,
                move.from_square,
                move.to_square,
                captured_piece,
            )

        self.reset_en_passant()

        if moving_piece.lower() == "p":
            if abs(from_row - to_row) == 2:
                middle_row = (from_row + to_row) // 2

                self.en_passant_target = position_to_square(
                    middle_row,
                    from_column,
                )

        if (
            moving_piece.lower() == "p"
            or captured_piece != Board.EMPTY
        ):
            self.halfmove_clock = 0
        else:
            self.halfmove_clock += 1

        if self.side_to_move == self.BLACK:
            self.fullmove_number += 1

        self.switch_side()

        return captured_piece

    def undo_move(self):
        if not self._undo_stack:
            raise ValueError("No move to undo")

        snapshot = self._undo_stack.pop()

        self._restore_snapshot(snapshot)

        if self.move_history:
            self.move_history.pop()