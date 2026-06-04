from typing import Optional

from piece import Piece
from square import *


class Board:
    def __init__(self, width: int, height: int):
        if width < 4 or height < 4:
            raise ValueError("Board dimensions must be at least 4x4")
        if width > 10 or height > 10:
            raise ValueError("Board dimensions must not exceed 10x10")
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
        
    def set_square(self, x: int, y: int, square: Square):
        if self.is_valid_position(x, y):
            self.board[y][x] = square
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
    
    def export_to_json(self) -> dict:
        return {
            "width": self.width,
            "height": self.height,
            "squares": [
                [square.get_code() for square in row] for row in self.board
            ],
            "pieces": [ 
                [str(square.piece) for square in row] for row in self.board
            ]
        }
    
    def reset_board(self):
        self.board = [[BasicSquare() for _ in range(self.width)] for _ in range(self.height)]
        

if __name__ == "__main__":
    board = Board(8, 8)
    board.set_square(0, 0, BasicSquare())
    board.set_square(1, 0, TeleportSquare())
    board.set_square(2, 0, TrapSquare())
    board.set_square(3, 0, HeartSquare())
    board.set_square(4, 0, ShieldSquare())
    board.set_square(5, 0, GrassSquare())
    board.set_piece(0, 0, Piece("Rook"))
    board.set_piece(1, 0, Piece("Knight"))
    board.set_piece(2, 0, Piece("Bishop"))
    board.set_piece(3, 0, Piece("Queen"))
    board.set_piece(4, 0, Piece("King"))
    board.set_piece(5, 0, Piece("Bishop"))
    board.set_piece(6, 0, Piece("Knight"))
    board.set_piece(7, 0, Piece("Rook"))
    
    for i in range(8):
        board.set_piece(i, 1, Piece("Pawn"))
    
    board.display()
    print()
    saved_state = board.export_to_json()
    print(saved_state)
    # print()
    # board.reset_board()
    # board.display()
    # board.import_from_json(board.export_to_json())
    # board.display()