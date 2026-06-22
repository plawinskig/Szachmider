from __future__ import annotations

import random
from typing import Any, Protocol, TYPE_CHECKING, cast, runtime_checkable

from source.bot.base_bot import BaseBot, BotMove, Move

if TYPE_CHECKING:
    from source.board.board import Board
    from source.board.piece import Piece


@runtime_checkable
class _BotPiece(Protocol):
    def is_black(self) -> bool:
        ...

    def get_ID(self) -> str:
        ...

    def get_code(self) -> str:
        ...


@runtime_checkable
class _BotBoard(Protocol):
    width: int
    height: int
    _board: list[list[Any]]

    def get_piece(self, x: int, y: int) -> _BotPiece | None:
        ...

    def get_available_move_packages(self, pieceID: str) -> list[Move]:
        ...


class GreedyBot(BaseBot):
    _piece_values: dict[str, int] = {
        "Paw": 100,
        "Kni": 300,
        "Bis": 320,
        "Roo": 500,
        "Que": 900,
        "Kin": 20_000,
    }

    def get_best_move(
        self,
        board: "Board",
        move_history: Any | None = None,
        time_limit: float | None = None,
    ) -> BotMove | None:
        if not isinstance(board, _BotBoard): # type: ignore
            return None

        scored_moves: list[tuple[float, BotMove]] = []

        for row in board._board:
            for square in row:
                if square is None:
                    continue

                piece = getattr(square, "piece", None)
                if not isinstance(piece, _BotPiece):
                    continue

                if piece.is_black() != self.is_black:
                    continue

                typed_piece = cast("Piece", piece)
                legal_moves = board.get_available_move_packages(piece.get_ID())
                for move in legal_moves:
                    score = self._score_move(board, piece, move)
                    scored_moves.append((score, (typed_piece, move)))

        if not scored_moves:
            return None

        best_score = max(score for score, _ in scored_moves)
        best_moves = [move for score, move in scored_moves if score == best_score]
        return random.choice(best_moves)

    def _score_move(self, board: _BotBoard, piece: _BotPiece, move: Move) -> float:
        target_x, target_y = move[0]
        captured_piece = board.get_piece(target_x, target_y)
        moving_value = self._get_piece_value(piece)
        score = 0.0

        return score

    def _get_piece_value(self, piece: _BotPiece) -> int:
        return self._piece_values.get(piece.get_code(), 100)

    def _get_pawn_progress_score(self, board: _BotBoard, piece: _BotPiece, target_y: int) -> float:
        if piece.is_black():
            return float(target_y) * 2.0
        return float(board.height - 1 - target_y) * 2.0

    def _get_center_score(self, board: _BotBoard, target_x: int, target_y: int) -> float:
        center_x = (board.width - 1) / 2
        center_y = (board.height - 1) / 2
        distance = abs(target_x - center_x) + abs(target_y - center_y)
        return max(0.0, 6.0 - distance)
