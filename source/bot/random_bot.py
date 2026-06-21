
from __future__ import annotations

import random
from typing import Any, Protocol, TYPE_CHECKING, cast, runtime_checkable

from source.bot.base_bot import BaseBot, BotMove, Move

if TYPE_CHECKING:
    from source.board.board import Board
    from source.board.piece import Piece


@runtime_checkable
class _MovablePiece(Protocol):
    def is_black(self) -> bool:
        ...

    def get_ID(self) -> str:
        ...


class RandomBot(BaseBot):
    def get_best_move(
        self,
        board: "Board",
        move_history: Any | None = None,
        time_limit: float | None = None,
    ) -> BotMove | None:
        available_moves: list[BotMove] = []

        for row in board._board:
            for square in row:
                if square is None:
                    continue

                piece = square.piece
                if not isinstance(piece, _MovablePiece): # type: ignore
                    continue

                if piece.is_black() != self.is_black:
                    continue

                typed_piece = cast("Piece", piece)
                legal_moves = board.get_available_move_packages(piece.get_ID())

                for move in legal_moves:
                    available_moves.append((typed_piece, move)) # type: ignore

        if not available_moves:
            return None

        return random.choice(available_moves)
