from engine.board import Board
from engine.move_generator import MoveGenerator


def main():
    board = Board()

    board.display()

    print("\nWhite pawn moves from e2:")

    moves = MoveGenerator.generate_pawn_moves(
        board,
        "e2"
    )

    for move in moves:
        print(move)

    print("\nWhite knight moves from g1:")

    moves = MoveGenerator.generate_knight_moves(
        board,
        "g1"
    )

    for move in moves:
        print(move)


if __name__ == "__main__":
    main()