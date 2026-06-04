from square import Square


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[Square() for _ in range(width)] for _ in range(height)]
        
    def get_square(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.board[y][x]
        else:
            raise IndexError("Square coordinates out of bounds")
    
    def move_piece(self, from_x, from_y, to_x, to_y):
        if (0 <= from_x < self.width and 
            0 <= from_y < self.height and 
            0 <= to_x < self.width and 
            0 <= to_y < self.height
            ):
            piece = self.board[from_y][from_x]
            self.board[to_y][to_x] = piece
            self.board[from_y][from_x] = Square()
        else:
            raise IndexError("Square coordinates out of bounds")
    
    def display(self):
        for row in self.board:
            print(" ".join(str(square) for square in row))
    
    def reset_board(self):
        self.board = [[Square() for _ in range(self.width)] for _ in range(self.height)]
        

