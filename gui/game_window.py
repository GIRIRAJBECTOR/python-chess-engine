import pygame
import copy
from engine.game_state import GameState
from gui.board_renderer import BoardRenderer
from engine.ai import ChessAI


class GameWindow:

    WIDTH = 640
    HEIGHT = 760
    BOARD_HEIGHT = 640
    FPS = 60

    STATUS_HEIGHT = 40
    HISTORY_HEIGHT = 40

    def __init__(self):

        pygame.init()

        self.screen = pygame.display.set_mode(
            (self.WIDTH, self.HEIGHT)
        )

        pygame.display.set_caption(
            "Python Chess Engine"
        )

        self.clock = pygame.time.Clock()

        self.running = True
        self.game_started = False
        self.game_mode = None

        # AI opponent: human plays White, engine plays Black.
        self.ai_side = GameState.BLACK
        self.ai = ChessAI(depth=2)
        self.ai_thinking = False
        self.ai_delay_until = None

        # -------------------------------------------------
        # Game state
        # -------------------------------------------------

        self.game_state = GameState()

        self.board_renderer = BoardRenderer(
            self.screen,
            self.game_state,
        )

        # -------------------------------------------------
        # Selection
        # -------------------------------------------------

        self.selected_square = None
        self.legal_moves = []

        # -------------------------------------------------
        # Move history
        # -------------------------------------------------

        self.move_history = []
        self.game_history = []
        self.ai_thinking = False
        self.ai_delay_until = None
        self.ai_thinking = False

        # -------------------------------------------------
        # Fonts
        # -------------------------------------------------

        self.status_font = pygame.font.Font(
            None,
            26,
        )

        self.history_font = pygame.font.Font(
            None,
            22,
        )

        self.button_font = pygame.font.Font(
            None,
            22,
        )

        self.menu_title_font = pygame.font.Font(None, 48)
        self.menu_button_font = pygame.font.Font(None, 30)

        # Start-menu buttons.
        self.computer_button = pygame.Rect(140, 300, 360, 70)
        self.human_button = pygame.Rect(140, 400, 360, 70)

        # -------------------------------------------------
        # Restart button
        # -------------------------------------------------

        self.restart_button = pygame.Rect(
            10,
            self.BOARD_HEIGHT + self.STATUS_HEIGHT + 4,
            120,
            32,
        )

        self.undo_button = pygame.Rect(
            135,
            self.BOARD_HEIGHT + self.STATUS_HEIGHT + 4,
            100,
            32,
        )

    # =====================================================
    # MOVE GENERATION
    # =====================================================

    def get_legal_moves_from_square(self, square):

        legal_moves = (
            self.game_state.generate_legal_moves()
        )

        return [
            move
            for move in legal_moves
            if str(move)[:2] == square
        ]

    # =====================================================
    # SELECTION
    # =====================================================

    def select_square(self, square):

        self.selected_square = square

        self.legal_moves = (
            self.get_legal_moves_from_square(
                square
            )
        )

        self.board_renderer.selected_square = square

        self.board_renderer.legal_squares = {
            str(move)[2:4]
            for move in self.legal_moves
        }

    def clear_selection(self):

        self.selected_square = None
        self.legal_moves = []

        self.board_renderer.selected_square = None
        self.board_renderer.legal_squares = set()

    # =====================================================
    # BOARD HELPERS
    # =====================================================

    def get_piece_at(self, square):

        row, column = (
            self.board_renderer.square_to_position(
                square
            )
        )

        return self.game_state.board.get_piece(
            row,
            column,
        )

    def is_current_player_piece(self, piece):

        if piece == ".":
            return False

        if self.game_state.side_to_move == GameState.WHITE:
            return piece.isupper()

        return piece.islower()

    # =====================================================
    # MOVE NOTATION
    # =====================================================

    def get_move_notation(self, move):

        move_text = str(move)
        from_square = move_text[:2]
        to_square = move_text[2:4]

        # Castling
        if from_square == "e1" and to_square == "g1":
            return "O-O"

        if from_square == "e1" and to_square == "c1":
            return "O-O-O"

        if from_square == "e8" and to_square == "g8":
            return "O-O"

        if from_square == "e8" and to_square == "c8":
            return "O-O-O"

        piece = self.get_piece_at(from_square)
        captured_piece = self.get_piece_at(to_square)

        if piece in (None, "."):
            piece = "P"

        piece_letter = {
            "K": "K",
            "Q": "Q",
            "R": "R",
            "B": "B",
            "N": "N",
            "P": "",
            "k": "K",
            "q": "Q",
            "r": "R",
            "b": "B",
            "n": "N",
            "p": "",
        }.get(piece, "")

        is_capture = captured_piece not in (None, ".")

        # En-passant capture: destination is empty, but a pawn moves diagonally.
        if piece.lower() == "p" and from_square[0] != to_square[0] and captured_piece in (None, "."):
            is_capture = True

        notation = piece_letter

        if piece.lower() == "p" and is_capture:
            notation += from_square[0]

        if is_capture:
            notation += "x"

        notation += to_square

        # Promotion. Different Move implementations may expose promotion
        # under one of these common attribute names.
        promotion = getattr(move, "promotion", None)
        if promotion is None:
            promotion = getattr(move, "promotion_piece", None)

        if promotion:
            promotion_map = {
                "q": "Q", "Q": "Q",
                "r": "R", "R": "R",
                "b": "B", "B": "B",
                "n": "N", "N": "N",
            }
            promotion = promotion_map.get(str(promotion), str(promotion).upper())
            notation += "=" + promotion

        return notation

    # =====================================================
    # MOVE HISTORY
    # =====================================================

    def add_move_to_history(self, move, notation=None):

        move_text = notation if notation is not None else self.get_move_notation(move)

        self.move_history.append(
            move_text
        )

    # =====================================================
    # START MENU
    # =====================================================

    def start_game(self, mode):
        self.game_mode = mode
        self.game_started = True

        self.game_state = GameState()
        self.board_renderer.game_state = self.game_state

        self.move_history = []
        self.game_history = []
        self.ai_thinking = False
        self.ai_delay_until = None
        self.clear_selection()

    def draw_start_menu(self):
        self.screen.fill((25, 25, 25))

        title = self.menu_title_font.render(
            "Python Chess Engine",
            True,
            (245, 245, 245),
        )
        title_rect = title.get_rect(
            center=(self.WIDTH // 2, 180)
        )
        self.screen.blit(title, title_rect)

        subtitle = self.button_font.render(
            "Choose game mode",
            True,
            (190, 190, 190),
        )
        subtitle_rect = subtitle.get_rect(
            center=(self.WIDTH // 2, 240)
        )
        self.screen.blit(subtitle, subtitle_rect)

        for rect, label in (
            (self.computer_button, "Computer vs Human"),
            (self.human_button, "Human vs Human"),
        ):
            pygame.draw.rect(
                self.screen,
                (70, 70, 70),
                rect,
                border_radius=10,
            )
            pygame.draw.rect(
                self.screen,
                (130, 130, 130),
                rect,
                2,
                border_radius=10,
            )

            text = self.menu_button_font.render(
                label,
                True,
                (255, 255, 255),
            )
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)

        pygame.display.flip()

    def handle_menu_click(self, mouse_pos):
        if self.computer_button.collidepoint(mouse_pos):
            # Human is White; computer is Black.
            self.ai_side = GameState.BLACK
            self.start_game("computer")
            return

        if self.human_button.collidepoint(mouse_pos):
            # No AI in two-player mode.
            self.ai_side = None
            self.start_game("human")
            return

    # =====================================================
    # RESTART
    # =====================================================

    def restart_game(self):

        self.game_state = GameState()

        # BoardRenderer must point to the new game state.
        self.board_renderer.game_state = (
            self.game_state
        )

        self.clear_selection()

        self.move_history = []
        self.game_history = []
        self.ai_thinking = False
        self.ai_delay_until = None

    # =====================================================
    # UNDO
    # =====================================================

    def undo_move(self):

        if not self.game_history:
            return

        self.ai_thinking = False
        self.ai_delay_until = None

        self.game_state = self.game_history.pop()
        self.board_renderer.game_state = self.game_state

        if self.move_history:
            self.move_history.pop()

        self.clear_selection()

    # =====================================================
    # MOUSE HANDLING
    # =====================================================

    def handle_mouse_click(self, mouse_pos):

        x, y = mouse_pos

        # -------------------------------------------------
        # Restart button
        # -------------------------------------------------

        if self.restart_button.collidepoint(
            mouse_pos
        ):

            self.restart_game()
            return

        if self.undo_button.collidepoint(
            mouse_pos
        ):

            self.undo_move()
            return

        # -------------------------------------------------
        # Ignore clicks outside board
        # -------------------------------------------------

        square = (
            self.board_renderer
            .get_square_from_mouse(mouse_pos)
        )

        if square is None:
            return

        # -------------------------------------------------
        # Don't allow moves while AI is waiting/thinking
        # -------------------------------------------------
        if self.ai_thinking:
            return

        # -------------------------------------------------
        # Don't allow moves after game is over
        # -------------------------------------------------

        if self.game_state.is_game_over():
            return

        # =================================================
        # NOTHING SELECTED
        # =================================================

        if self.selected_square is None:

            piece = self.get_piece_at(square)

            if self.is_current_player_piece(
                piece
            ):

                self.select_square(square)

            return

        # =================================================
        # TRY TO MOVE
        # =================================================

        target_move = None

        for move in self.legal_moves:

            if str(move)[2:4] == square:

                target_move = move
                break

        if target_move is not None:
            # One undo checkpoint represents the human move + AI reply.
            self.game_history.append(copy.deepcopy(self.game_state))

            notation = self.get_move_notation(target_move)
            self.game_state.make_move(target_move)

            next_side = self.game_state.side_to_move
            if self.game_state.is_checkmate(next_side):
                notation += "#"
            elif self.game_state.is_in_check(next_side):
                notation += "+"

            self.add_move_to_history(target_move, notation)
            self.clear_selection()

            # Schedule the AI reply 5 seconds after the human move.
            # Do not use sleep(): the pygame event loop must remain responsive.
            if (
                self.game_mode == "computer"
                and self.game_state.side_to_move == self.ai_side
                and not self.game_state.is_game_over()
            ):
                self.ai_thinking = True
                self.ai_delay_until = pygame.time.get_ticks() + 5000

            return

        # =================================================
        # SELECT ANOTHER OWN PIECE
        # =================================================

        piece = self.get_piece_at(square)

        if self.is_current_player_piece(
            piece
        ):

            self.select_square(square)

            return

        # =================================================
        # CLEAR SELECTION
        # =================================================

        self.clear_selection()

    # =====================================================
    # AI MOVE
    # =====================================================

    def make_ai_move(self):
        if self.game_state.side_to_move != self.ai_side:
            self.ai_thinking = False
            self.ai_delay_until = None
            return

        if self.game_state.is_game_over():
            self.ai_thinking = False
            self.ai_delay_until = None
            return

        try:
            move = self.ai.choose_move(self.game_state)
            if move is None:
                return

            notation = self.get_move_notation(move)
            self.game_state.make_move(move)

            next_side = self.game_state.side_to_move
            if self.game_state.is_checkmate(next_side):
                notation += "#"
            elif self.game_state.is_in_check(next_side):
                notation += "+"

            self.add_move_to_history(move, notation)
            self.clear_selection()
        finally:
            self.ai_thinking = False
            self.ai_delay_until = None

    def update_ai(self):
        if not self.ai_thinking:
            return

        if self.ai_delay_until is not None:
            if pygame.time.get_ticks() < self.ai_delay_until:
                return
            self.ai_delay_until = None

        self.make_ai_move()

    # =====================================================
    # STATUS
    # =====================================================

    def get_status_text(self):

        # -------------------------------------------------
        # Checkmate
        # -------------------------------------------------

        if self.game_state.is_checkmate(
            self.game_state.side_to_move
        ):

            if (
                self.game_state.side_to_move
                == GameState.WHITE
            ):

                return "Checkmate - Black wins"

            return "Checkmate - White wins"

        # -------------------------------------------------
        # Stalemate
        # -------------------------------------------------

        if self.game_state.is_stalemate(
            self.game_state.side_to_move
        ):

            return "Stalemate - Draw"

        # -------------------------------------------------
        # Check
        # -------------------------------------------------

        if self.game_state.is_in_check(
            self.game_state.side_to_move
        ):

            if (
                self.game_state.side_to_move
                == GameState.WHITE
            ):

                return "White to move - CHECK"

            return "Black to move - CHECK"

        # -------------------------------------------------
        # AI turn
        # -------------------------------------------------
        if self.ai_thinking:
            return "Black (AI) is thinking..."

        # -------------------------------------------------
        # Normal turn
        # -------------------------------------------------

        if (
            self.game_state.side_to_move
            == GameState.WHITE
        ):

            return "White to move"

        return "Black to move"

    # =====================================================
    # STATUS DRAW
    # =====================================================

    def draw_status(self):

        pygame.draw.rect(
            self.screen,
            (35, 35, 35),
            (
                0,
                self.BOARD_HEIGHT,
                self.WIDTH,
                self.STATUS_HEIGHT,
            ),
        )

        text = self.status_font.render(
            self.get_status_text(),
            True,
            (240, 240, 240),
        )

        text_rect = text.get_rect(
            center=(
                self.WIDTH // 2,
                self.BOARD_HEIGHT
                + self.STATUS_HEIGHT // 2,
            )
        )

        self.screen.blit(
            text,
            text_rect,
        )

    # =====================================================
    # MOVE HISTORY DRAW
    # =====================================================

    def draw_move_history(self):

        history_y = (
            self.BOARD_HEIGHT
            + self.STATUS_HEIGHT
        )

        pygame.draw.rect(
            self.screen,
            (25, 25, 25),
            (
                0,
                history_y,
                self.WIDTH,
                self.HISTORY_HEIGHT,
            ),
        )

        # -------------------------------------------------
        # Restart button
        # -------------------------------------------------

        pygame.draw.rect(
            self.screen,
            (70, 70, 70),
            self.restart_button,
            border_radius=6,
        )

        restart_text = self.button_font.render(
            "Restart",
            True,
            (255, 255, 255),
        )

        restart_rect = restart_text.get_rect(
            center=self.restart_button.center
        )

        self.screen.blit(
            restart_text,
            restart_rect,
        )

        pygame.draw.rect(
            self.screen,
            (70, 70, 70),
            self.undo_button,
            border_radius=6,
        )

        undo_text = self.button_font.render(
            "Undo",
            True,
            (255, 255, 255),
        )

        undo_rect = undo_text.get_rect(
            center=self.undo_button.center
        )

        self.screen.blit(
            undo_text,
            undo_rect,
        )

        # -------------------------------------------------
        # History text
        # -------------------------------------------------

        history_text = self.get_history_text()

        text = self.history_font.render(
            history_text,
            True,
            (230, 230, 230),
        )

        text_rect = text.get_rect(
            midleft=(
                250,
                history_y
                + self.HISTORY_HEIGHT // 2,
            )
        )

        self.screen.blit(
            text,
            text_rect,
        )

    # =====================================================
    # HISTORY STRING
    # =====================================================

    def get_history_text(self):

        if not self.move_history:
            return "Moves: -"

        moves = []

        for index, move in enumerate(
            self.move_history
        ):

            move_number = index // 2 + 1

            if index % 2 == 0:

                moves.append(
                    f"{move_number}.{move}"
                )

            else:

                moves[-1] += f" {move}"

        # Show only the last few moves so the
        # bottom UI doesn't become overcrowded.

        visible_moves = moves[-4:]

        return "Moves: " + "  ".join(
            visible_moves
        )

    # =====================================================
    # EVENTS
    # =====================================================

    def handle_events(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False
                continue

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not self.game_started:
                    self.handle_menu_click(event.pos)
                else:
                    self.handle_mouse_click(event.pos)

    # =====================================================
    # CHECK INDICATOR
    # =====================================================

    def get_king_square(self, side):

        king = "K" if side == GameState.WHITE else "k"

        for row in range(8):
            for column in range(8):
                if self.game_state.board.get_piece(row, column) == king:
                    return row, column

        return None

    def draw_check_indicator(self):

        side = self.game_state.side_to_move

        if not self.game_state.is_in_check(side):
            return

        king_position = self.get_king_square(side)

        if king_position is None:
            return

        row, column = king_position
        square_size = self.BOARD_HEIGHT // 8

        # Draw a red translucent overlay around the king's square.
        overlay = pygame.Surface(
            (square_size, square_size),
            pygame.SRCALPHA,
        )

        pygame.draw.rect(
            overlay,
            (220, 40, 40, 85),
            overlay.get_rect(),
        )

        pygame.draw.rect(
            overlay,
            (220, 40, 40, 230),
            overlay.get_rect(),
            5,
        )

        self.screen.blit(
            overlay,
            (column * square_size, row * square_size),
        )

    # =====================================================
    # GAME OVER OVERLAY
    # =====================================================

    def draw_game_over_overlay(self):

        if not self.game_state.is_game_over():
            return

        overlay = pygame.Surface(
            (self.WIDTH, self.BOARD_HEIGHT),
            pygame.SRCALPHA,
        )
        overlay.fill((0, 0, 0, 125))
        self.screen.blit(overlay, (0, 0))

        if self.game_state.is_checkmate(self.game_state.side_to_move):
            if self.game_state.side_to_move == GameState.WHITE:
                message = "CHECKMATE - BLACK WINS"
            else:
                message = "CHECKMATE - WHITE WINS"
        else:
            message = "STALEMATE - DRAW"

        font = pygame.font.Font(None, 42)
        text = font.render(message, True, (255, 255, 255))
        rect = text.get_rect(center=(self.WIDTH // 2, self.BOARD_HEIGHT // 2))

        panel = pygame.Rect(
            rect.x - 24,
            rect.y - 18,
            rect.width + 48,
            rect.height + 36,
        )
        pygame.draw.rect(self.screen, (25, 25, 25), panel, border_radius=10)
        pygame.draw.rect(self.screen, (220, 220, 220), panel, 2, border_radius=10)
        self.screen.blit(text, rect)

    # =====================================================
    # DRAW
    # =====================================================

    def draw(self):

        if not self.game_started:
            self.draw_start_menu()
            return

        self.board_renderer.draw()

        self.draw_check_indicator()

        self.draw_game_over_overlay()

        self.draw_status()

        self.draw_move_history()

        pygame.display.flip()

    # =====================================================
    # MAIN LOOP
    # =====================================================

    def run(self):

        while self.running:

            self.handle_events()

            self.update_ai()

            self.draw()

            self.clock.tick(
                self.FPS
            )

        pygame.quit()