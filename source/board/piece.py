from abc import ABC, abstractmethod
import source.board.pieceMovement as pieceMovement

class Piece(ABC):
    instanceCounter = 0
    def __init__(self, isBlack: bool):
        self._sprite: str
        self.moveIterators: list[pieceMovement.MovementIter]
        self.conditionalMoves: list # TODO
        self._isBlack: bool = isBlack
        self._pieceID: str = f"{self.get_code()}_{type(self).instanceCounter}_{"B" if self._isBlack else "W"}"
        self._moveRestriction: list[tuple[int, int]] = []
        self._allPossibleMoves: list[tuple[int, int]] = []

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
        return [x for x in self._allPossibleMoves if x in self._moveRestriction]

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
            pieceMovement.MoveVectorDir((1, 0), True),
            pieceMovement.MoveVectorDir((-1, 0), True),
            pieceMovement.MoveVectorDir((0, 1), True),
            pieceMovement.MoveVectorDir((0, -1), True)
        ]

    def get_code(self):
        return "Roo"




class Knight(Piece):
    instanceCounter = 0

    def __init__(self, isBlack: bool):
        super().__init__(isBlack)
        self.moveIterators = [
            pieceMovement.MoveVectorSymmetrical((3, 1), True)
        ]

    def get_code(self):
        return "Kni"

class Bishop(Piece):
    instanceCounter = 0

    def __init__(self, isBlack: bool):
        super().__init__(isBlack)

        self.moveIterators = [
            pieceMovement.MoveVectorDir((1, 1), True),
            pieceMovement.MoveVectorDir((-1, 1), True),
            pieceMovement.MoveVectorDir((1, -1), True),
            pieceMovement.MoveVectorDir((-1, -1), True)
        ]


    def get_code(self):
        return "Bis"

class Queen(Piece):
    instanceCounter = 0

    def __init__(self, isBlack: bool):
        super().__init__(isBlack)

        self.moveIterators = [
            pieceMovement.MoveVectorDir((1, 1), True),
            pieceMovement.MoveVectorDir((-1, 1), True),
            pieceMovement.MoveVectorDir((1, -1), True),
            pieceMovement.MoveVectorDir((-1, -1), True),

            pieceMovement.MoveVectorDir((1, 0), True),
            pieceMovement.MoveVectorDir((-1, 0), True),
            pieceMovement.MoveVectorDir((0, 1), True),
            pieceMovement.MoveVectorDir((0, -1), True)
        ]


    def get_code(self):
        return "Que"

class King(Piece):
    instanceCounter = 0

    def __init__(self, isBlack: bool):
        super().__init__(isBlack)
        self.__moved = False


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
            ], True)
        ]
        self._pieceID = f"Kin_{"B" if self._isBlack else "W"}"

    def get_code(self):
        return "Kin"

class Pawn(Piece):
    instanceCounter = 0

    def __init__(self, isBlack: bool):
        super().__init__(isBlack)
        self.__justMovedTwo = False
        self.__moved = False
        self.__direction = (1 if self._isBlack else -1)

        self.moveIterators = [
            pieceMovement.MoveVectorList([(0, self.__direction)], False)
        ]


    def get_code(self):
        return "Paw"




if __name__ == "__main__":
    l = [Rook(True), Rook(False), Rook(True), Knight(True), Bishop(False)]
    for p in l:
        print(p.get_ID())