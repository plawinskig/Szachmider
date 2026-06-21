import unittest
from typing import Any, cast
from unittest.mock import patch

from source.bot.base_bot import Move
from source.bot.random_bot import RandomBot


class FakePiece:
    def __init__(self, is_black: bool, moves: list[Move]) -> None:
        self._is_black = is_black
        self._moves = moves

    def is_black(self) -> bool:
        return self._is_black

    def get_actual_move_list(self) -> list[Move]:
        return self._moves


class FakeSquare:
    def __init__(self, piece: FakePiece | None = None) -> None:
        self.piece = piece


class FakeBoard:
    def __init__(self, rows: list[list[FakeSquare | None]]) -> None:
        self._board = rows


def make_board(rows: list[list[FakeSquare | None]]) -> Any:
    return cast(Any, FakeBoard(rows))


def make_move(target_x: int, target_y: int) -> Move:
    def execute_move() -> None:
        raise AssertionError("Bot must not execute the selected move lambda.")

    return ((target_x, target_y), execute_move, False)


class RandomBotTests(unittest.TestCase):
    def test_returns_none_when_board_has_no_pieces(self) -> None:
        board = make_board(
            [
                [FakeSquare(), FakeSquare()],
                [FakeSquare(), None],
            ]
        )

        result = RandomBot(is_black=False).get_best_move(board)

        self.assertIsNone(result)

    def test_returns_none_when_own_pieces_have_no_legal_moves(self) -> None:
        white_piece = FakePiece(is_black=False, moves=[])
        black_piece = FakePiece(is_black=True, moves=[make_move(1, 1)])
        board = make_board([[FakeSquare(white_piece), FakeSquare(black_piece)]])

        result = RandomBot(is_black=False).get_best_move(board)

        self.assertIsNone(result)

    def test_chooses_only_moves_owned_by_bot_color(self) -> None:
        white_move = make_move(0, 1)
        black_move = make_move(1, 1)
        white_piece = FakePiece(is_black=False, moves=[white_move])
        black_piece = FakePiece(is_black=True, moves=[black_move])
        board = make_board([[FakeSquare(white_piece), FakeSquare(black_piece)]])

        with patch("source.bot.random_bot.random.choice", side_effect=lambda moves: moves[0]):
            selected_piece, selected_move = RandomBot(is_black=False).get_best_move(board)

        self.assertIs(selected_piece, white_piece)
        self.assertIs(selected_move, white_move)

    def test_includes_every_legal_move_from_matching_pieces_in_random_pool(self) -> None:
        first_move = make_move(0, 1)
        second_move = make_move(1, 1)
        third_move = make_move(2, 1)
        first_piece = FakePiece(is_black=True, moves=[first_move, second_move])
        second_piece = FakePiece(is_black=True, moves=[third_move])
        board = make_board([[FakeSquare(first_piece), FakeSquare(second_piece)]])
        captured_pool: list[tuple[FakePiece, Move]] = []

        def choose_last_move(moves: list[tuple[FakePiece, Move]]) -> tuple[FakePiece, Move]:
            captured_pool.extend(moves)
            return moves[-1]

        with patch("source.bot.random_bot.random.choice", side_effect=choose_last_move):
            selected_piece, selected_move = RandomBot(is_black=True).get_best_move(board)

        self.assertEqual(
            captured_pool,
            [
                (first_piece, first_move),
                (first_piece, second_move),
                (second_piece, third_move),
            ],
        )
        self.assertIs(selected_piece, second_piece)
        self.assertIs(selected_move, third_move)

    def test_does_not_execute_move_lambda(self) -> None:
        move_was_executed = False

        def execute_move() -> None:
            nonlocal move_was_executed
            move_was_executed = True

        move: Move = ((3, 4), execute_move, True)
        piece = FakePiece(is_black=False, moves=[move])
        board = make_board([[FakeSquare(piece)]])

        result = RandomBot(is_black=False).get_best_move(board)

        self.assertIsNotNone(result)
        self.assertFalse(move_was_executed)


if __name__ == "__main__":
    unittest.main()
