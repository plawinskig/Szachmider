from typing import Optional

from piece import Piece
from square import Square


class Board:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.reset_board()
        
    def get_square(self, x: int, y: int) -> Square:
        if self.is_valid_position(x, y):
            return self.board[y][x]
        else:
            raise IndexError("Square coordinates out of bounds")
    
    def get_piece(self, x: int, y: int) -> Optional[Piece]:
        square = self.get_square(x, y)
        return square.piece if square else None
        
    def set_square(self, x: int, y: int, piece: Square):
        if self.is_valid_position(x, y):
            self.board[y][x] = piece
        else:
            raise IndexError("Square coordinates out of bounds")
    
    def set_piece(self, x: int, y: int, piece: Piece):
        square = self.get_square(x, y)
        
        if square:
            square.piece = piece
        else:
            raise IndexError("Square coordinates out of bounds")
    
    def move_piece(self, from_x: int, from_y: int, to_x: int, to_y: int):
        piece = self.get_piece(from_x, from_y)
        
        if piece is None:
            raise ValueError("No piece at the source square")
        
        if not self.is_valid_move(from_x, from_y, to_x, to_y):
            raise ValueError("Invalid move")
        
        self.set_piece(to_x, to_y, piece)
        self.set_square(from_x, from_y, Square())
    
    def is_empty_square(self, x: int, y: int) -> bool:
        square = self.get_square(x, y)
        return square.is_empty() if square else False
    
    def is_valid_position(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height
    
    def is_valid_move(self, from_x: int, from_y: int, to_x: int, to_y: int) -> bool:
        return True # TODO
    
    def display(self):
        for row in self.board:
            print(" ".join(str(square) for square in row))
    
    def reset_board(self):
        self.board = [[Square() for _ in range(self.width)] for _ in range(self.height)]
        

