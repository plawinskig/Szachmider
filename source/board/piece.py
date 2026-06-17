from abc import ABC, abstractmethod
from source.board.move import Move
# Gives error for circular imports
#from source.board.board import Board

class Piece(ABC):
    def __init__(self, is_black: bool):
        self._is_black = is_black
        self.has_moved = False
    
    def __str__(self):
        return self.__class__.__name__
    
    def is_black(self) -> bool:
        return self._is_black
    
    def get_ID(self) -> str:
        return self.get_code() + ("B" if self.is_black() else "W")
    
    @abstractmethod
    def get_code(self) -> str:
        pass

    @abstractmethod
    def can_move(self, board: Board, move: Move) -> bool:
        pass

class Rook(Piece):
    def get_code(self) -> str:
        return "Roo"
    
    def can_move(self, board: Board, move: Move) -> bool:
        return True

class Knight(Piece):
    def get_code(self) -> str:
        return "Kni"
    
    def can_move(self, board: Board, move: Move) -> bool:
        return True

class Bishop(Piece):
    def get_code(self) -> str:
        return "Bis"
    
    def can_move(self, board: Board, move: Move) -> bool:
        return True

class Queen(Piece):
    def get_code(self) -> str:
        return "Que"
    
    def can_move(self, board: Board, move: Move) -> bool:
        return True

class King(Piece):
    def get_code(self) -> str:
        return "Kin"
    
    def can_move(self, board: Board, move: Move) -> bool:
        return True

class Pawn(Piece):
    def get_code(self) -> str:
        return "Paw"
    
    def can_move(self, board: Board, move: Move) -> bool:
        return True
    