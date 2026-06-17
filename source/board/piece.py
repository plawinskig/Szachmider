from abc import ABC, abstractmethod
from typing import Callable, Any

from board import Board


import pieceMovement

class Piece(ABC):
    instanceCounter = 0
    def __init__(self, isBlack: bool):
        self._sprite: str
        self.moveIterators: list[pieceMovement.MovementIter]
        # self.conditionalMoves: list[tuple[pieceMovement.MovementIter, Callable[[tuple[str, ...], dict[str, Any]], bool]]] # TODO
        self._isBlack: bool = isBlack
        self._pieceID: str = f"{self.get_code()}_{type(self).instanceCounter}_{"B" if self._isBlack else "W"}"
        self._moveRestriction: list[tuple[int, int]] = []
        self._allPossibleMoves: list[tuple[Callable[..., Any], tuple[int, int]]] = []
        self._moveCounter = 0

        type(self).instanceCounter += 1

    def __str__(self):
        return self.__class__.__name__

    def get_ID(self):
        return self._pieceID

    def is_black(self):
        return self._isBlack

    def set_restrictions(self, restr: list[tuple[int, int]]):
        self._moveRestriction.clear()
        self._moveRestriction = restr.copy()

    def clear_restrictions(self):
        self._moveRestriction.clear()

    def add_possible_moves(self, newMoves):
        self._allPossibleMoves.extend(newMoves)

    def clear_possible_moves(self):
        self._allPossibleMoves.clear()

    def get_actual_move_list(self):
        if self._moveRestriction == []: return self._allPossibleMoves
        return [x for x in self._allPossibleMoves if x[0] in self._moveRestriction]

    def inc_move_counter(self):
        self._moveCounter += 1

    def check_special_moves(self, theEntireBoard: Board, location: tuple[int, int]):
        pass

    @abstractmethod
    def get_code(self):
        pass


    def debug_print_moves(self):
        print(f"moves: {self._allPossibleMoves}")
        print(f"restriction: {self._moveRestriction}")




class Rook(Piece):
    instanceCounter = 0

    def __init__(self, isBlack: bool):
        super().__init__(isBlack)

        self.moveIterators = [
            pieceMovement.MoveVectorDir((1, 0)),
            pieceMovement.MoveVectorDir((-1, 0)),
            pieceMovement.MoveVectorDir((0, 1)),
            pieceMovement.MoveVectorDir((0, -1))
        ]

    def get_code(self):
        return "Roo"




class Knight(Piece):
    instanceCounter = 0

    def __init__(self, isBlack: bool):
        super().__init__(isBlack)
        self.moveIterators = [
            pieceMovement.MoveVectorSymmetrical((2, 1), True)
        ]

    def get_code(self):
        return "Kni"

class Bishop(Piece):
    instanceCounter = 0

    def __init__(self, isBlack: bool):
        super().__init__(isBlack)

        self.moveIterators = [
            pieceMovement.MoveVectorDir((1, 1)),
            pieceMovement.MoveVectorDir((-1, 1)),
            pieceMovement.MoveVectorDir((1, -1)),
            pieceMovement.MoveVectorDir((-1, -1))
        ]


    def get_code(self):
        return "Bis"

class Queen(Piece):
    instanceCounter = 0

    def __init__(self, isBlack: bool):
        super().__init__(isBlack)

        self.moveIterators = [
            pieceMovement.MoveVectorDir((1, 1)),
            pieceMovement.MoveVectorDir((-1, 1)),
            pieceMovement.MoveVectorDir((1, -1)),
            pieceMovement.MoveVectorDir((-1, -1)),

            pieceMovement.MoveVectorDir((1, 0)),
            pieceMovement.MoveVectorDir((-1, 0)),
            pieceMovement.MoveVectorDir((0, 1)),
            pieceMovement.MoveVectorDir((0, -1))
        ]


    def get_code(self):
        return "Que"

class King(Piece):
    instanceCounter = 0

    def __init__(self, isBlack: bool):
        super().__init__(isBlack)

        self.moveIterators = [
            pieceMovement.MoveVectorList([
                (0, 1),
                (1, 0),
                (1, 1),
                (-1, 0),
                (-1, -1),
                (0, -1),
                (-1, 1),
                (1, -1)
            ])
        ]
        self._pieceID = f"Kin_{"B" if self._isBlack else "W"}"

    def get_code(self):
        return "Kin"

class Pawn(Piece):
    instanceCounter = 0

    def __init__(self, isBlack: bool):
        super().__init__(isBlack)
        self.__movedTwo = False

        self.__direction = (1 if self._isBlack else -1)

        self.moveIterators = [
            pieceMovement.MoveVectorList([(0, self.__direction)], canTake=False),
            pieceMovement.MoveVectorList([(1, self.__direction), (-1, self.__direction)], canMove=False)
        ]

    def __do_en_passant(self, board: Board, location: tuple[int, int], moveToLocation: tuple[int, int], target: tuple[int, int]):
        board.move_piece(*location, *moveToLocation)
        board.take_piece(*target)

    def __do_double_move(self, board: Board, from_x: int, from_y: int, to_x: int, to_y: int):
        board.move_piece(from_x, from_y, to_x, to_y)
        self.__movedTwo = True

    def check_special_moves(self, theEntireBoard: Board, location: tuple[int, int]):
        validMoves = []

        x, y = location
        # double move
        dMove = (x, y + 2*self.__direction)
        if self._moveCounter == 0 and not(dMove[1] < 0 or dMove[1] >= theEntireBoard.height) and theEntireBoard.get_piece(*dMove) == None:
            validMoves.append((dMove, lambda : self.__do_double_move(theEntireBoard, x, y, *dMove)))


        # en passant
        #
        #
        # for target in [(x-1, y), (x+1, y)]:
        #     if not(target[0] < 0 or target[0] >= theEntireBoard.width):
        #         targetPiece = theEntireBoard.get_piece(*target)
        #         if targetPiece.get_code() == "Pwn" and targetPiece.is_black() != self._isBlack and targetPiece._moveCounter == 1 and targetPiece.__movedTwo:
        #             validMoves.append((
        #                 (target[0], target[1] + self.__direction),
        #                 lambda : self.__do_en_passant(theEntireBoard, location, (target[0], target[1] + self.__direction), target)
        #             ))

        return validMoves

    def get_code(self):
        return "Paw"





