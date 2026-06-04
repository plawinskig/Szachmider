

class Square:
    def __init__(self, piece=None):
        self.piece = piece
        
    def is_empty(self):
        return self.piece is None
    
    def __str__(self):
        return str(self.piece) if self.piece else "."

