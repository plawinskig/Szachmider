from abc import ABC, abstractmethod

from piece import *


class Square(ABC):
    def __init__(self, piece: Piece = None):
        self.piece = piece
        
    def is_empty(self):
        return self.piece is None
    
    def __str__(self):
        return self.__class__.__name__
    
    @abstractmethod
    def get_code(self):
        pass
    
    @abstractmethod
    def get_functionality(self):
        pass


class BasicSquare(Square):
    def __init__(self, piece: Piece = None):
        super().__init__(piece)
        
    def get_code(self):
        return "Bsc"
        
    def get_functionality(self):
        return "Basic functionality"

class TeleportSquare(Square):
    def __init__(self, tele: tuple[int, int], piece: Piece = None):
        super().__init__(piece)
        self.__teleLocation = tele


    def get_tele_location(self):
        return self.__teleLocation


    def get_code(self):
        return "Tel"
        
    def get_functionality(self):
        return "Teleport functionality"
        

class TrapSquare(Square):
    def __init__(self, piece: Piece = None):
        super().__init__(piece)
        
    def get_code(self):
        return "Tra"
        
    def get_functionality(self):
        return "Trap functionality"


class HeartSquare(Square):
    def __init__(self, piece: Piece = None):
        super().__init__(piece)
        
    def get_code(self):
        return "Hrt"
        
    def get_functionality(self):
        return "Heart functionality"


class ShieldSquare(Square):
    def __init__(self, piece: Piece = None):
        super().__init__(piece)
        
    def get_code(self):
        return "Shl"
        
    def get_functionality(self):
        return "Shield functionality"


class GrassSquare(Square):
    def __init__(self, piece: Piece = None):
        super().__init__(piece)
    
    def get_code(self):
        return "Grs"
        
    def get_functionality(self):
        return "Grass functionality"

