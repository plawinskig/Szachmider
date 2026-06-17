from dataclasses import dataclass

@dataclass(frozen=True)
class Move:
    from_x: int
    from_y: int
    to_x: int
    to_y: int

