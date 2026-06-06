import os
from typing import Optional, Any

from piece import *
from square import *
from board_json import save_to_json
from move import Move
from obj_mapping import square_mapping, piece_mapping

class Board:
    def __init__(self, width: int, height: int):
        if width < 4 or height < 4:
            raise ValueError("Board dimensions must be at least 4x4")
        if width > 10 or height > 10:
            raise ValueError("Board dimensions must not exceed 10x10")
        self.width = width
        self.height = height
        
        self.last_move: Optional[tuple[Piece, Move]] = None
        
        self.board: list[list[Square]] = []
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
    
    def set_piece(self, x: int, y: int, piece: Optional[Piece]):
        square = self.get_square(x, y)
        
        if square:
            square.piece = piece
        else:
            raise IndexError("Square coordinates out of bounds")
    
    def is_empty_square(self, x: int, y: int) -> bool:
        square = self.get_square(x, y)
        return square.is_empty() if square else False
    
    def is_valid_position(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height
    
    def is_valid_move(self, move: Move) -> bool:
        from_x, from_y, to_x, to_y = move.from_x, move.from_y, move.to_x, move.to_y
        if not (self.is_valid_position(from_x, from_y) and self.is_valid_position(to_x, to_y)):
            return False

        if from_x == to_x and from_y == to_y:
            return False
        
        moving_piece = self.get_piece(from_x, from_y)
        if moving_piece is None:
            return False

        target_piece = self.get_piece(to_x, to_y)
        if target_piece is not None and target_piece.color == moving_piece.color:
            return False
        
        if not moving_piece.can_move(move):
            return False
        
        return True
    
    def move_piece(self, move: Move):
        from_x, from_y, to_x, to_y = move.from_x, move.from_y, move.to_x, move.to_y
        moving_piece = self.get_piece(from_x, from_y)
        
        if moving_piece is None:
            raise ValueError("No piece at the source square")
        
        if not self.is_valid_move(move):
            raise ValueError("Invalid move")
        
        # en passant
        if moving_piece.get_code() == "Pwn" and from_x != to_x and self.is_empty_square(to_x, to_y):
            self.set_piece(to_x, from_y, None)
        
        # castleling
        if moving_piece.get_code() == "Kin" and abs(to_x - from_x) == 2:
            self._handle_castling(move)
        
        self.set_piece(to_x, to_y, moving_piece)
        self.set_piece(from_x, from_y, None)
        
        moving_piece.has_moved = True
        self.last_move = (moving_piece, move)
    
    def _handle_castling(self, move: Move):
        if move.from_y != move.to_y:
            raise ValueError("Invalid castling move: King must move horizontally")
        
        from_x, to_x, y = move.from_x, move.to_x, move.from_y
        
        # short castle
        if to_x > from_x:
            rook_from_x = self.width - 1
            rook_to_x = to_x - 1
        # long castle
        else:
            rook_from_x = 0
            rook_to_x = to_x + 1
            
        rook = self.get_piece(rook_from_x, y)
        if rook:
            self.set_piece(rook_to_x, y, rook)
            self.set_piece(rook_from_x, y, None)
            rook.has_moved = True
        else:
            raise ValueError("Invalid castling move: Rook not found")
    
    def is_square_attacked(self, x: int, y: int, enemy_color: str) -> bool:
        for row_y in range(self.height):
            for col_x in range(self.width):
                enemy_piece = self.get_piece(col_x, row_y)
                
                if enemy_piece and enemy_piece.color == enemy_color:
                    if enemy_piece.can_move(Move(col_x, row_y, x, y)):
                        return True
        return False
    
    def is_path_clear(self, move: Move) -> bool:
        from_x, from_y, to_x, to_y = move.from_x, move.from_y, move.to_x, move.to_y
        step_x = 0 if from_x == to_x else (1 if to_x > from_x else -1)
        step_y = 0 if from_y == to_y else (1 if to_y > from_y else -1)
        
        curr_x = from_x + step_x
        curr_y = from_y + step_y
        while curr_x != to_x or curr_y != to_y:
            if not self.is_empty_square(curr_x, curr_y):
                return False
            curr_x += step_x
            curr_y += step_y
        
        return True
    
    def display(self):
        for row in self.board:
            print(" ".join(str(square) for square in row))
    
    def export_to_json(self) -> dict[str, Any]:
        return {
            "width": self.width,
            "height": self.height,
            "squares": [
                [square.get_code() for square in row] for row in self.board
            ],
            "pieces": [ 
                [square.piece.get_code() if square.piece else None for square in row] for row in self.board
            ]
        }
        
    def import_from_json(self, data: dict[str, Any]):
        self.width = data["width"]
        self.height = data["height"]
        self.last_move = None 
        
        self.board = []
        for y in range(self.height):
            row: list[Square] = []
            for x in range(self.width):
                sq_code = data["squares"][y][x]
                square_class = square_mapping.get(sq_code, BasicSquare)
                square = square_class()
                
                p_code = data["pieces"][y][x]
                if p_code and piece_mapping.get(p_code):
                    square.piece = piece_mapping[p_code]()
                    
                row.append(square)
            self.board.append(row)
    
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
    board.set_piece(0, 0, Rook())
    board.set_piece(1, 0, Knight())
    board.set_piece(2, 0, Bishop())
    board.set_piece(3, 0, Queen())
    board.set_piece(4, 0, King())
    board.set_piece(5, 0, Bishop())
    board.set_piece(6, 0, Knight())
    board.set_piece(7, 0, Rook())
    
    for i in range(8):
        board.set_piece(i, 1, Pawn())
    
    board.display()
    print()
    saved_state = board.export_to_json()
    save_to_json(saved_state, "boards" + os.sep + "board_state.json")
    # print()
    # board.reset_board()
    # board.display()
    # board.import_from_json(board.export_to_json())
    # board.display()