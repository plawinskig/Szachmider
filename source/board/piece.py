from abc import ABC, abstractmethod

class Piece(ABC):
    def __str__(self):
        return self.__class__.__name__
    
    @abstractmethod
    def get_code(self) -> str:
        pass

class Rook(Piece):
    def get_code(self) -> str:
        return "Roo"
    
class Knight(Piece):
    def get_code(self) -> str:
        return "Kni"

class Bishop(Piece):
    def get_code(self) -> str:
        return "Bis"

class Queen(Piece):
    def get_code(self) -> str:
        return "Que"

class King(Piece):
    def get_code(self) -> str:
        return "Kin"

class Pawn(Piece):
    def get_code(self) -> str:
        return "Paw"