import pygame

from engine.board import Board


class BoardRenderer:
    BOARD_SIZE = 640
    SQUARE_SIZE = BOARD_SIZE // 8

    LIGHT_SQUARE = (240, 217, 181)
    DARK_SQUARE = (181, 136, 99)

    SELECTED_COLOR = (246, 246, 105)
    LEGAL_MOVE_COLOR = (100, 180, 100)

    COORDINATE_COLOR = (80, 80, 80)

    PIECES = {
        "K": "♔",
        "Q": "♕",
        "R": "♖",
        "B": "♗",
        "N": "♘",
        "P": "♙",
        "k": "♚",
        "q": "♛",
        "r": "♜",
        "b": "♝",
        "n": "♞",
        "p": "♟",
    }

    def __init__(self, screen, game_state):
        self.screen = screen
        self.game_state = game_state

        self.piece_font = pygame.font.SysFont(
            "Segoe UI Symbol",
            64
        )

        self.coordinate_font = pygame.font.Font(
            None,
            20
        )

        self.selected_square = None
        self.legal_squares = set()

    def draw_board(self):
        for row in range(8):
            for column in range(8):

                color = (
                    self.LIGHT_SQUARE
                    if (row + column) % 2 == 0
                    else self.DARK_SQUARE
                )

                pygame.draw.rect(
                    self.screen,
                    color,
                    (
                        column * self.SQUARE_SIZE,
                        row * self.SQUARE_SIZE,
                        self.SQUARE_SIZE,
                        self.SQUARE_SIZE,
                    ),
                )

    def draw_highlights(self):

        if self.selected_square:
            row, column = self.square_to_position(
                self.selected_square
            )

            pygame.draw.rect(
                self.screen,
                self.SELECTED_COLOR,
                (
                    column * self.SQUARE_SIZE,
                    row * self.SQUARE_SIZE,
                    self.SQUARE_SIZE,
                    self.SQUARE_SIZE,
                ),
                5,
            )

        for square in self.legal_squares:

            row, column = self.square_to_position(square)

            center = (
                column * self.SQUARE_SIZE
                + self.SQUARE_SIZE // 2,
                row * self.SQUARE_SIZE
                + self.SQUARE_SIZE // 2,
            )

            pygame.draw.circle(
                self.screen,
                self.LEGAL_MOVE_COLOR,
                center,
                10,
            )

    def draw_coordinates(self):

        for column in range(8):

            file_name = chr(ord("a") + column)

            text = self.coordinate_font.render(
                file_name,
                True,
                self.COORDINATE_COLOR,
            )

            x = column * self.SQUARE_SIZE + 5
            y = self.BOARD_SIZE - 20

            self.screen.blit(text, (x, y))

        for row in range(8):

            rank = str(8 - row)

            text = self.coordinate_font.render(
                rank,
                True,
                self.COORDINATE_COLOR,
            )

            x = 5
            y = row * self.SQUARE_SIZE + 5

            self.screen.blit(text, (x, y))

    def draw_pieces(self):

        for row in range(8):
            for column in range(8):

                piece = self.game_state.board.get_piece(
                    row,
                    column,
                )

                if piece == Board.EMPTY:
                    continue

                symbol = self.PIECES.get(piece)

                if symbol is None:
                    continue

                text = self.piece_font.render(
                    symbol,
                    True,
                    (20, 20, 20),
                )

                text_rect = text.get_rect(
                    center=(
                        column * self.SQUARE_SIZE
                        + self.SQUARE_SIZE // 2,

                        row * self.SQUARE_SIZE
                        + self.SQUARE_SIZE // 2,
                    )
                )

                self.screen.blit(text, text_rect)

    def position_to_square(self, row, column):

        file_name = chr(ord("a") + column)
        rank = str(8 - row)

        return file_name + rank

    def square_to_position(self, square):

        column = ord(square[0]) - ord("a")
        row = 8 - int(square[1])

        return row, column

    def get_square_from_mouse(self, mouse_pos):

        x, y = mouse_pos

        column = x // self.SQUARE_SIZE
        row = y // self.SQUARE_SIZE

        if not (0 <= row < 8 and 0 <= column < 8):
            return None

        return self.position_to_square(
            row,
            column,
        )

    def draw(self):

        self.draw_board()
        self.draw_highlights()
        self.draw_coordinates()
        self.draw_pieces()