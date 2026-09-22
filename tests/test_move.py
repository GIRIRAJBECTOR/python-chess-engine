from engine.move import Move


def test_normal_move():
    move = Move("e2", "e4")

    assert move.from_square == "e2"
    assert move.to_square == "e4"
    assert move.promotion is None
    assert str(move) == "e2e4"


def test_promotion_move():
    move = Move("e7", "e8", "Q")

    assert move.promotion == "Q"
    assert str(move) == "e7e8Q"