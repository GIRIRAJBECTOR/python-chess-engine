from dataclasses import dataclass


@dataclass(frozen=True)
class Move:
    from_square: str
    to_square: str
    promotion: str | None = None

    def __str__(self):
        if self.promotion:
            return f"{self.from_square}{self.to_square}{self.promotion}"

        return f"{self.from_square}{self.to_square}"