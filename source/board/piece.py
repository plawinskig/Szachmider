from abc import ABC, abstractmethod
from typing import Callable, Any
from functools import partial

import source.board.board as board
import source.board.pieceMovement as pieceMovement 

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

    @abstractmethod
    def get_code(self):
        pass

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


    # treat it like a specialized, conditional part of Boarc.__get_piece_moves()
    # make sure it handles move restrictions, bcs the main function won't do it
    def check_special_moves(self, theEntireBoard: board.Board, location: tuple[int, int]) -> tuple[
        list[tuple[tuple[int, int], Callable[[] ,None], bool]], #plausible moves
        list[tuple[int, int]], # checks
        list[tuple[int, int]] # additional checks
        ]:
        return [], [], []




    def debug_print_moves(self):
        print(f"moves: {self._allPossibleMoves}")
        print(f"restriction: {self._moveRestriction}")




class Rook(Piece):
    instanceCounter = 0

    def __init__(self, isBlack: bool):
        super().__init__(isBlack)
        if self._isBlack:
            self._sprite = "assets/pieces/Rook_dark.png"
        else:
            self._sprite = "assets/pieces/Rook_light.png"

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
        if self._isBlack:
            self._sprite = "assets/pieces/Knight_dark.png"
        else:
            self._sprite = "assets/pieces/Knight_light.png"

        self.moveIterators = [
            pieceMovement.MoveVectorSymmetrical((2, 1), True)
        ]

    def get_code(self):
        return "Kni"
    


class Bishop(Piece):
    instanceCounter = 0

    def __init__(self, isBlack: bool):
        super().__init__(isBlack)
        if self._isBlack:
            self._sprite = "assets/pieces/Bishop_dark.png"
        else:
            self._sprite = "assets/pieces/Bishop_light.png"

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
        if self._isBlack:
            self._sprite = "assets/pieces/Queen_dark.png"
        else:
            self._sprite = "assets/pieces/Queen_light.png"

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
        if self._isBlack:
            self._sprite = "assets/pieces/King_dark.png"
        else:
            self._sprite = "assets/pieces/King_light.png"

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
    



    def __do_castle(self, board: board.Board, location: tuple[int, int], rookLocation: tuple[int, int], direction: int):
        board.move_piece(*location, location[0] + 2*direction, location[1])
        board.move_piece(*rookLocation, location[0] + direction, location[1])


    def check_castling(self, theEntireBoard: board.Board, location: tuple[int, int], otherColorMoveMatrix: list[list[list[tuple[str, Callable[[], None], bool]]]]):
        castles = []
        if self._moveCounter > 0 or otherColorMoveMatrix[location[1]][location[0]] != []:
            return castles

        for dir in [-1, 1]:
            moves = pieceMovement.MoveVectorDir((dir, 0))(*location)
            allow = True
            rookLocation = None
            steps = 0
            for move in moves:
                # print(move)
                if move[0] < 0 or move[0] >= theEntireBoard.width:
                    break
                steps += 1

                potentialAttack = otherColorMoveMatrix[move[1]][move[0]]
                attacked = False
                for at in potentialAttack:
                    if at[2]:
                        attacked = True

                if attacked:
                    allow = False

                nextSquare = theEntireBoard.get_square(*move)
                if nextSquare is None:
                    allow = False
                    break

                nextPiece = theEntireBoard.get_piece(*move)
                if not nextPiece is None:
                    if nextPiece.get_code() == "Roo" and self.is_black() == nextPiece.is_black() and nextPiece._moveCounter == 0:
                        rookLocation = move
                    else:
                        allow = False

            if steps < 3 or rookLocation is None:
                allow = False

            if allow:
                castles.append(
                    (
                        (location[0] + 2*dir, location[1]), 
                        partial(self.__do_castle, theEntireBoard, location, rookLocation, dir), # type: ignore
                        False
                    )
                )
        # print(castles)
        return castles



class Pawn(Piece):
    instanceCounter = 0

    def __init__(self, isBlack: bool):
        super().__init__(isBlack)
        if self._isBlack:
            self._sprite = "assets/pieces/Pawn_dark.png"
        else:
            self._sprite = "assets/pieces/Pawn_light.png"

        self.__movedTwo = False

        self.__direction = (1 if self._isBlack else -1)

        self.moveIterators = [
            pieceMovement.MoveVectorList([(0, self.__direction)], canTake=False),
            pieceMovement.MoveVectorList([(1, self.__direction), (-1, self.__direction)], canMove=False)
        ]

    #
    # def __do_en_passant(self, board: board.Board, location: tuple[int, int], moveToLocation: tuple[int, int], target: tuple[int, int]):
    #     board.move_piece(*location, *moveToLocation)
    #     board.take_piece(*target)
    #


    def __do_double_move(self, board: board.Board, from_x: int, from_y: int, to_x: int, to_y: int):
        board.move_piece(from_x, from_y, to_x, to_y)
        self.__movedTwo = True

    def check_special_moves(self, theEntireBoard: board.Board, location: tuple[int, int]):
        validMoves = []

        x, y = location
        # double move
        dMove = (x, y + 2*self.__direction)
        if self._moveCounter == 0 and not(dMove[1] < 0 or dMove[1] >= theEntireBoard.height) and theEntireBoard.get_piece(*dMove) is None:
            validMoves.append((dMove, partial(self.__do_double_move, theEntireBoard, x, y, *dMove), False))


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

        return validMoves, [], []

    def get_code(self):
        return "Paw"





