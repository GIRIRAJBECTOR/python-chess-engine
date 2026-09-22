class Board:
    EMPTY = "."

    def __init__(self):
        self.board = self._create_initial_board()

    def _create_initial_board(self):
        return [
            ["r", "n", "b", "q", "k", "b", "n", "r"],
            ["p", "p", "p", "p", "p", "p", "p", "p"],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            ["P", "P", "P", "P", "P", "P", "P", "P"],
            ["R", "N", "B", "Q", "K", "B", "N", "R"],
        ]

    def get_piece(self, row, column):
        return self.board[row][column]

    def set_piece(self, row, column, piece):
        self.board[row][column] = piece

    def display(self):
        print("  a b c d e f g h")
        print("  ----------------")

        for row in range(8):
            rank = 8 - row
            pieces = " ".join(self.board[row])
            print(f"{rank}|{pieces}|")

        print("  ----------------")
        print("  a b c d e f g h")