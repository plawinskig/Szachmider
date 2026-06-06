from abc import ABC, abstractmethod

class Piece(ABC):
    def __init__(self):
        self.color = "White"
    
    def __str__(self):
        return self.__class__.__name__
    
    @abstractmethod
    def get_code(self) -> str:
        pass

    @abstractmethod
    def can_move(self, from_x: int, from_y: int, to_x: int, to_y: int) -> bool:
        pass

class Rook(Piece):
    def get_code(self) -> str:
        return "Roo"
    
    def can_move(self, from_x: int, from_y: int, to_x: int, to_y: int) -> bool:
        return True

class Knight(Piece):
    def get_code(self) -> str:
        return "Kni"
    
    def can_move(self, from_x: int, from_y: int, to_x: int, to_y: int) -> bool:
        return True

class Bishop(Piece):
    def get_code(self) -> str:
        return "Bis"
    
    def can_move(self, from_x: int, from_y: int, to_x: int, to_y: int) -> bool:
        return True

class Queen(Piece):
    def get_code(self) -> str:
        return "Que"
    
    def can_move(self, from_x: int, from_y: int, to_x: int, to_y: int) -> bool:
        return True

class King(Piece):
    def get_code(self) -> str:
        return "Kin"
    
    def can_move(self, from_x: int, from_y: int, to_x: int, to_y: int) -> bool:
        return True

class Pawn(Piece):
    def get_code(self) -> str:
        return "Paw"
    
    def can_move(self, from_x: int, from_y: int, to_x: int, to_y: int) -> bool:
        return True
    