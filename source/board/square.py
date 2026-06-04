from piece import Piece


class Square:
    def __init__(self, piece: Piece = Piece()):
        self.piece = piece
        
    def is_empty(self):
        return self.piece is None
    
    def __str__(self):
        return str(self.piece) if self.piece else "."


class BasicSquare(Square):
    def __init__(self, piece: Piece = Piece()):
        super().__init__(piece)


class TeleportSquare(Square):
    def __init__(self, piece: Piece = Piece()):
        super().__init__(piece)
        

class TrapSquare(Square):
    def __init__(self, piece: Piece = Piece()):
        super().__init__(piece)


class HeartSquare(Square):
    def __init__(self, piece: Piece = Piece()):
        super().__init__(piece)


class ShieldSquare(Square):
    def __init__(self, piece: Piece = Piece()):
        super().__init__(piece)


class GrassSquare(Square):
    def __init__(self, piece: Piece = Piece()):
        super().__init__(piece)

