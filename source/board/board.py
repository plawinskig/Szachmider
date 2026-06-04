from square import Square


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.reset_board()
        
    def get_square(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.board[y][x]
        else:
            raise IndexError("Square coordinates out of bounds")
        
    def set_square(self, x, y, piece):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.board[y][x] = piece
        else:
            raise IndexError("Square coordinates out of bounds")
    
    def move_piece(self, from_x, from_y, to_x, to_y):
        piece = self.get_square(from_x, from_y)
        self.set_square(to_x, to_y, piece)
        self.set_square(from_x, from_y, Square())
    
    def display(self):
        for row in self.board:
            print(" ".join(str(square) for square in row))
    
    def reset_board(self):
        self.board = [[Square() for _ in range(self.width)] for _ in range(self.height)]
        

