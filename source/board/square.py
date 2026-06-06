from abc import ABC, abstractmethod

from piece import Piece
from typing import Optional


class Square(ABC):
    def __init__(self, piece: Optional[Piece] = None):
        self.piece = piece
        
    def is_empty(self) -> bool:
        return self.piece is None
    
    def __str__(self):
        return self.__class__.__name__
    
    @abstractmethod
    def get_code(self) -> str:
        pass
    
    @abstractmethod
    def get_functionality(self) -> str:
        pass


class BasicSquare(Square):
    def __init__(self, piece: Optional[Piece] = None):
        super().__init__(piece)
        
    def get_code(self) -> str:
        return "Bsc"
        
    def get_functionality(self) -> str:
        return "Basic functionality"

class TeleportSquare(Square):
    def __init__(self, piece: Optional[Piece] = None):
        super().__init__(piece)
        
    def get_code(self) -> str:
        return "Tel"
        
    def get_functionality(self) -> str:
        return "Teleport functionality"
        

class TrapSquare(Square):
    def __init__(self, piece: Optional[Piece] = None):
        super().__init__(piece)
        
    def get_code(self) -> str:
        return "Tra"
        
    def get_functionality(self) -> str:
        return "Trap functionality"


class HeartSquare(Square):
    def __init__(self, piece: Optional[Piece] = None):
        super().__init__(piece)
        
    def get_code(self) -> str:
        return "Hrt"
        
    def get_functionality(self) -> str:
        return "Heart functionality"


class ShieldSquare(Square):
    def __init__(self, piece: Optional[Piece] = None):
        super().__init__(piece)
        
    def get_code(self) -> str:
        return "Shl"
        
    def get_functionality(self) -> str:
        return "Shield functionality"


class GrassSquare(Square):
    def __init__(self, piece: Optional[Piece] = None):
        super().__init__(piece)
    
    def get_code(self) -> str:
        return "Grs"
        
    def get_functionality(self) -> str:
        return "Grass functionality"

