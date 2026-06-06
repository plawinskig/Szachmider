from abc import ABC, abstractmethod

class Piece(ABC):
    def __init__(self):
        self._sprite: str

    def __str__(self):
        return self.__class__.__name__
    
    @abstractmethod
    def get_code(self):
        pass

class Rook(Piece):
    def get_code(self):
        return "Roo"
    
class Knight(Piece):
    def get_code(self):
        return "Kni"

class Bishop(Piece):
    def get_code(self):
        return "Bis"

class Queen(Piece):
    def get_code(self):
        return "Que"

class King(Piece):
    def get_code(self):
        return "Kin"

class Pawn(Piece):
    def get_code(self):
        return "Paw"