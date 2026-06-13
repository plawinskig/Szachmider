from abc import ABC, abstractmethod
import pieceMovement

class Piece(ABC):
    def __init__(self):
        self._sprite: str
        self.moveIterators: list[pieceMovement.MovementIter]
        self.conditionalMoves: list # TODO
        self._pieceID: str
        self._isBlack: bool

    def __str__(self):
        return self.__class__.__name__

    def get_ID(self):
        return self._pieceID
    
    @abstractmethod
    def get_code(self):
        pass




class Rook(Piece):
    instanceCounter = 0

    def __init__(self, isBlack: bool):
        self._isBlack = isBlack

        Rook.instanceCounter += 1

        self.moveIterators = [
            pieceMovement.MoveVectorDir((1, 0), False),
            pieceMovement.MoveVectorDir((-1, 0), False),
            pieceMovement.MoveVectorDir((0, 1), False),
            pieceMovement.MoveVectorDir((0, -1), False)
        ]

        self._pieceID = f"{self.get_code()}_{Rook.instanceCounter}_{"B" if self._isBlack else "W"}"


    def get_code(self):
        return "Roo"




class Knight(Piece):
    instanceCounter = 0

    def __init__(self, isBlack: bool):
        self._isBlack = isBlack

        Knight.instanceCounter += 1

        self.moveIterators = [
            pieceMovement.MoveVectorSymmetrical((3, 1))
        ]

        self._pieceID = f"{self.get_code()}_{Knight.instanceCounter}_{"B" if self._isBlack else "W"}"

    def get_code(self):
        return "Kni"

class Bishop(Piece):
    instanceCounter = 0

    def __init__(self, isBlack: bool):
        self._isBlack = isBlack

        Bishop.instanceCounter += 1

        self.moveIterators = [
            pieceMovement.MoveVectorDir((1, 1), False),
            pieceMovement.MoveVectorDir((-1, 1), False),
            pieceMovement.MoveVectorDir((1, -1), False),
            pieceMovement.MoveVectorDir((-1, -1), False)
        ]

        self._pieceID = f"{self.get_code()}_{Bishop.instanceCounter}_{"B" if self._isBlack else "W"}"


    def get_code(self):
        return "Bis"

class Queen(Piece):
    instanceCounter = 0

    def __init__(self, isBlack: bool):
        self._isBlack = isBlack

        Queen.instanceCounter += 1

        self.moveIterators = [
            pieceMovement.MoveVectorDir((1, 1), False),
            pieceMovement.MoveVectorDir((-1, 1), False),
            pieceMovement.MoveVectorDir((1, -1), False),
            pieceMovement.MoveVectorDir((-1, -1), False),

            pieceMovement.MoveVectorDir((1, 0), False),
            pieceMovement.MoveVectorDir((-1, 0), False),
            pieceMovement.MoveVectorDir((0, 1), False),
            pieceMovement.MoveVectorDir((0, -1), False)
        ]

        self._pieceID = f"{self.get_code()}_{Queen.instanceCounter}_{"B" if self._isBlack else "W"}"

    def get_code(self):
        return "Que"

class King(Piece):
    instanceCounter = 0

    def __init__(self, isBlack: bool):
        self.__moved = False
        self._isBlack = isBlack

        King.instanceCounter += 1

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

        self._pieceID = f"{self.get_code()}_{King.instanceCounter}_{"B" if self._isBlack else "W"}"



    def get_code(self):
        return "Kin"

class Pawn(Piece):
    instanceCounter = 0

    def __init__(self, isBlack: bool):
        self.__justMovedTwo = False
        self.__moved = False
        self._isBlack = isBlack
        self.__direction = (1 if self._isBlack else -1)

        Pawn.instanceCounter += 1

        self.moveIterators = [
            pieceMovement.MoveVectorList([(0, self.__direction),])
        ]

        self._pieceID = f"{self.get_code()}_{Pawn.instanceCounter}_{"B" if self._isBlack else "W"}"

    def get_code(self):
        return "Paw"