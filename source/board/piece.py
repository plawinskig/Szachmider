from abc import ABC, abstractmethod

class Piece:
    def __str__(self):
        return self.__class__.__name__
    
    @abstractmethod
    def get_code(self):
        pass

class Rook(Piece):
    def get_code(self):
        return "R"
    
class Knight(Piece):
    def get_code(self):
        return "N"

class Bishop(Piece):
    def get_code(self):
        return "B"

class Queen(Piece):
    def get_code(self):
        return "Q"

class King(Piece):
    def get_code(self):
        return "K"

class Pawn(Piece):
    def get_code(self):
        return "P"