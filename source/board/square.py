from source.pieces.piece import Piece


class Square:
    def __init__(self, piece: Piece = Piece()):
        self.piece = piece
        
    def is_empty(self):
        return self.piece is None
    
    def __str__(self):
        return str(self.piece) if self.piece else "."

