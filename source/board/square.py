from abc import ABC, abstractmethod

from source.board.piece import Piece
from typing import Optional


class Square(ABC):
    def __init__(self, piece: Optional[Piece] = None):
        self.piece = piece
        self.img_tile_light = None
        self.img_tile_dark = None
        self.img_back_light = None
        self.img_back_dark = None
        self.img_front_light = None
        self.img_front_dark = None
        
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
        self.img_tile_light = "assets/squares/SQR_tile_basic_light.png"
        self.img_tile_dark = "assets/squares/SQR_tile_basic_dark.png"
        self.img_back_light = None
        self.img_back_dark = None
        self.img_front_light = None
        self.img_front_dark = None
        
    def get_code(self) -> str:
        return "Bsc"
        
    def get_functionality(self) -> str:
        return "Basic functionality"

class TeleportSquare(Square):
    def __init__(self, tele: tuple[int, int], piece: Optional[Piece] = None):
        super().__init__(piece)
        self.img_tile_light = "assets/squares/SQR_tile_teleporter_light.png"
        self.img_tile_dark = "assets/squares/SQR_tile_teleporter_dark.png"
        self.img_back_light = "assets/squares/SQR_tile_teleporter_back.png"
        self.img_back_dark = self.img_back_light
        self.img_front_light = "assets/squares/SQR_tile_teleporter_front.png"
        self.img_front_dark = self.img_front_light
        self.__teleLocation = tele


    def get_tele_location(self):
        return self.__teleLocation


    def get_code(self) -> str:
        return "Tel"
        
    def get_functionality(self) -> str:
        return "Teleport functionality"
        

class TrapSquare(Square):
    def __init__(self, piece: Optional[Piece] = None):
        super().__init__(piece)
        self.img_tile_light = "assets/squares/SQR_tile_trap_light.png"
        self.img_tile_dark = "assets/squares/SQR_tile_trap_dark.png"
        self.img_back_light = "assets/squares/SQR_tile_trap_back.png"
        self.img_back_dark = self.img_back_light
        self.img_front_light = "assets/squares/SQR_tile_trap_front.png"
        self.img_front_dark = self.img_front_light

    def get_code(self) -> str:
        return "Tra"
        
    def get_functionality(self) -> str:
        return "Trap functionality"


class HeartSquare(Square):
    def __init__(self, piece: Optional[Piece] = None):
        super().__init__(piece)
        self.img_tile_light = "assets/squares/SQR_tile_heart_light.png"
        self.img_tile_dark = "assets/squares/SQR_tile_heart_dark.png"
        self.img_back_light = None
        self.img_back_dark = None
        self.img_front_light = "assets/squares/SQR_tile_heart_front.png"
        self.img_front_dark = self.img_front_light
        
    def get_code(self) -> str:
        return "Hrt"
        
    def get_functionality(self) -> str:
        return "Heart functionality"


class ShieldSquare(Square):
    def __init__(self, piece: Optional[Piece] = None):
        super().__init__(piece)
        self.img_tile_light = "assets/squares/SQR_tile_metal_light.png"
        self.img_tile_dark = "assets/squares/SQR_tile_metal_dark.png"
        self.img_back_light = None
        self.img_back_dark = None
        self.img_front_light = "assets/squares/SQR_tile_metal_front.png"
        self.img_front_dark = self.img_front_light

    def get_code(self) -> str:
        return "Shl"
        
    def get_functionality(self) -> str:
        return "Shield functionality"


class GrassSquare(Square):
    def __init__(self, piece: Optional[Piece] = None):
        super().__init__(piece)
        self.img_tile_light = "assets/squares/SQR_tile_grass_light.png"
        self.img_tile_dark = "assets/squares/SQR_tile_grass_dark.png"
        self.img_back_light = "assets/squares/SQR_tile_grass_light_back.png"
        self.img_back_dark = "assets/squares/SQR_tile_grass_dark_back.png"
        self.img_front_light = "assets/squares/SQR_tile_grass_light_front.png"
        self.img_front_dark = "assets/squares/SQR_tile_grass_dark_front.png"
    
    def get_code(self) -> str:
        return "Grs"
        
    def get_functionality(self) -> str:
        return "Grass functionality"

