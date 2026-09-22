FILES = "abcdefgh"


def square_to_position(square):
    """
    Convert chess notation such as 'e4' into
    internal board coordinates (row, column).
    """

    if not isinstance(square, str) or len(square) != 2:
        raise ValueError(f"Invalid square: {square}")

    file = square[0].lower()
    rank = square[1]

    if file not in FILES or rank not in "12345678":
        raise ValueError(f"Invalid square: {square}")

    column = FILES.index(file)
    row = 8 - int(rank)

    return row, column


def position_to_square(row, column):
    """
    Convert internal board coordinates into chess notation.
    """

    if not (0 <= row < 8 and 0 <= column < 8):
        raise ValueError("Position outside board")

    file = FILES[column]
    rank = str(8 - row)

    return file + rank