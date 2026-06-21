
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from source.board.board import Board
    from source.board.piece import Piece

Move = tuple[tuple[int, int], Callable[[], None], bool]
BotMove = tuple["Piece", Move]


class BaseBot(ABC):
    def __init__(self, is_black: bool) -> None:
        self.is_black = is_black

    @abstractmethod
    def get_best_move(
        self,
        board: "Board",
        move_history: Any | None = None,
        time_limit: float | None = None,
    ) -> BotMove | None:
        raise NotImplementedError
