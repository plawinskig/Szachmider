import os
import types
from typing import Optional, Any

from source.board.piece import Piece, Rook, Knight, Bishop, Queen, King, Pawn
from source.board.square import Square, BasicSquare, TeleportSquare, TrapSquare, HeartSquare, ShieldSquare, GrassSquare
from source.board.board_json import save_to_json
from source.board.move import Move
from source.board.obj_mapping import SQUARE_MAP, PIECE_MAP

class Board:
    def __init__(self, width: int, height: int):
        if width < 4 or height < 4:
            raise ValueError("Board dimensions must be at least 4x4")
        if width > 10 or height > 10:
            raise ValueError("Board dimensions must not exceed 10x10")
            
        self._width = width
        self._height = height
        self._last_move: Optional[tuple[Piece, Move]] = None
        self._board: list[list[Square]] = []
        
        self.reset_board()

        self.__whiteMoveMatrix = [[[] for _ in range(self.width)] for _ in range(self.height)]
        self.__blackMoveMatrix = [[[] for _ in range(self.width)] for _ in range(self.height)]
        
    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def last_move(self) -> Optional[tuple[Piece, Move]]:
        return self._last_move
        
    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def last_move(self) -> Optional[tuple[Piece, Move]]:
        return self._last_move
        
    def get_square(self, x: int, y: int) -> Square:
        if self.is_valid_position(x, y):
            return self._board[y][x]
        else:
            raise IndexError("Square coordinates out of bounds")
    
    def get_piece(self, x: int, y: int) -> Optional[Piece]:
        square = self.get_square(x, y)
        return square.piece if square else None
        
    def set_square(self, x: int, y: int, square: Square):
        if self.is_valid_position(x, y):
            self._board[y][x] = square
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
        return 0 <= x < self._width and 0 <= y < self._height
    
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
        if target_piece is not None and target_piece.is_black() == moving_piece.is_black():
            return False
        
        if not moving_piece.can_move(self, move):
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
        if moving_piece.get_code() == "Paw" and from_x != to_x and self.is_empty_square(to_x, to_y):
            self.set_piece(to_x, from_y, None)
        
        # castleling
        if moving_piece.get_code() == "Kin" and abs(to_x - from_x) == 2:
            self._handle_castling(move)
        
        self.set_piece(to_x, to_y, moving_piece)
        self.set_piece(from_x, from_y, None)
        
        moving_piece.has_moved = True
        self._last_move = (moving_piece, move)
    
    def _handle_castling(self, move: Move):
        if move.from_y != move.to_y:
            raise ValueError("Invalid castling move: King must move horizontally")
        
        from_x, to_x, y = move.from_x, move.to_x, move.from_y
        
        # short castle
        if to_x > from_x:
            rook_from_x = self._width - 1
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
    
    def is_square_attacked(self, x: int, y: int, enemy_is_black: bool) -> bool:
        for row_y in range(self._height):
            for col_x in range(self._width):
                enemy_piece = self.get_piece(col_x, row_y)
                
                if enemy_piece and enemy_piece.is_black() == enemy_is_black:
                    test_move = Move(col_x, row_y, x, y)
                    if enemy_piece.can_move(self, test_move):
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
        for row in self._board:
            print(" ".join(str(square) for square in row))
    
    def export_to_json(self) -> dict[str, Any]:
        squares_data: list[list[str]] = []
        pieces_data: list[list[dict[str, Any] | None]] = []

        for row in self._board:
            row_squares: list[str] = []
            row_pieces: list[dict[str, Any] | None] = []
            for square in row:
                row_squares.append(square.get_code())
                
                if square.piece:
                    piece_code = square.piece.get_code()
                    piece_state: dict[str, Any] = {
                        "type": piece_code,
                        "isBlack": square.piece.is_black(),
                        "id": square.piece.get_ID(),
                    }

                    if piece_code == "Kin":
                        piece_state["moved"] = getattr(square.piece, "_King__moved", False)
                    elif piece_code == "Paw":
                        piece_state["moved"] = getattr(square.piece, "_Pawn__moved", False)
                        piece_state["justMovedTwo"] = getattr(square.piece, "_Pawn__justMovedTwo", False)       
                        
                    row_pieces.append(piece_state)
                else:
                    row_pieces.append(None)
                    
            squares_data.append(row_squares)
            pieces_data.append(row_pieces)

        return {
            "width": self._width,
            "height": self._height,
            "squares": squares_data,
            "pieces": pieces_data
        }
        
    def import_from_json(self, data: dict[str, Any]):
        self._width = data["width"]
        self._height = data["height"]
        
        self.reset_board() 
        
        for y in range(self._height):
            for x in range(self._width):
                square_code = data["squares"][y][x]
                square_class = SQUARE_MAP.get(square_code, BasicSquare) 
                new_square = square_class()
                
                piece_data = data["pieces"][y][x]
                if piece_data is not None:
                    piece_type = piece_data["type"]
                    piece_class = PIECE_MAP.get(piece_type)
                    if piece_class:
                        new_piece = piece_class(isBlack=piece_data["isBlack"])
                        
                        new_piece._pieceID = piece_data["id"] 

                        if piece_type == "Kin":
                            setattr(new_piece, "_King__moved", piece_data["moved"])
                        elif piece_type == "Paw":
                            setattr(new_piece, "_Pawn__moved", piece_data["moved"])
                            setattr(new_piece, "_Pawn__justMovedTwo", piece_data["justMovedTwo"])
                            
                        new_square.piece = new_piece
                
                self._board[y][x] = new_square
                
        self.make_movement_matrix()
        
    def make_movement_matrix(self):
        pass
    
    def reset_board(self):
        self.board = [[BasicSquare() for _ in range(self.width)] for _ in range(self.height)]


    def iterate_board(self):
        for boardY in range(self.height):
            for boardX in range(self.width):
                yield (boardX, boardY, self.get_square(boardX, boardY), self.get_piece(boardX, boardY))



    def __get_piece_moves(self):
        kings = []
        pieces = []
        whiteChecks = []
        blackChecks = []

        for place in self.iterate_board():
            boardX, boardY, currentSquare, currentPiece = place
            if  currentPiece == None:
                continue

            if isinstance(currentPiece, King): # król jest ewaluowany na końcu żeby nie wszedł w szacha
                kings.append((boardX, boardY))
                continue

            currentPiece.clear_possible_moves()

            pieces.append(currentPiece)

            for moveIter in currentPiece.moveIterators:
                moveInstance = iter(moveIter)(boardX, boardY)

                encounteredPieces = []
                foundKing = False

                plausibleMoves = [] # legalne ruchy iteratora
                canGoFurther = True
                theoriticalMoves = [] # wszystkie ruchy iteratora - do tworzenia oraniczeń

                for move in moveInstance:
                    if move[0] < 0 or move[0] >= self.width or move[1] < 0 or move[1] >= self.height:
                        break

                    nextSquare = self.get_square(move[0], move[1])
                    nextPiece = self.get_piece(move[0], move[1])
                    # print(nextPiece, move)

                    if nextPiece != None:
                        if moveIter.can_take() and nextSquare.get_code() != "Shl" and currentSquare.get_code() != "Hrt" and nextPiece.is_black() != currentPiece.is_black():
                            theoriticalMoves.append(move)
                            if canGoFurther: plausibleMoves.append(move)
                            if not foundKing: encounteredPieces.append(nextPiece)
                            if isinstance(nextPiece, King):
                                foundKing = True

                        canGoFurther = moveIter.jumps_over() or nextSquare.get_code() == "Grs"
                    else:
                        if not foundKing: theoriticalMoves.append(move)
                        if canGoFurther: plausibleMoves.append(move)



                print(plausibleMoves)
                currentPiece.add_possible_moves(plausibleMoves)

                if foundKing and len(encounteredPieces) == 2:
                    restricedPiece = encounteredPieces[0]
                    if isinstance(restricedPiece, King): restricedPiece = encounteredPieces[1]
                    theoriticalMoves.append((boardX, boardY))
                    restricedPiece.set_restrictions(theoriticalMoves)
                elif foundKing and len(encounteredPieces) == 1:
                    theoriticalMoves.append((boardX, boardY))
                    if currentPiece.is_black():
                        blackChecks.append(theoriticalMoves)
                    else:
                        whiteChecks.append(theoriticalMoves)



            if currentSquare.get_code() == "Tel":
                currentPiece.add_possible_moves([currentSquare.get_tele_location()])

        return kings, pieces, blackChecks, whiteChecks



    def __blocks_check(self, checks: list[list[tuple[int, int]]], move: tuple[int, int]):
        blocks = False
        for i in checks:
            if move in i:
                blocks = True

        return blocks

    def make_movement_matrix(self):
        self.__whiteMoveMatrix = [[[] for _ in range(self.width)] for _ in range(self.height)]
        self.__blackMoveMatrix = [[[] for _ in range(self.width)] for _ in range(self.height)]


        kings, pieces, blackChecks, whiteChecks = self.__get_piece_moves()
        for p in pieces:
            p.debug_print_moves()
            for move in p.get_actual_move_list():
                if p.is_black():
                    self.__blackMoveMatrix[move[1]][move[0]].append(p.get_ID())
                else:
                    self.__whiteMoveMatrix[move[1]][move[0]].append(p.get_ID())

        otherKing = ""
        for k in kings:
            currentKing = self.get_piece(*k)
            kingIter = iter(currentKing.moveIterators[0])(*k)

            for move in kingIter:
                if currentKing.is_black():
                    attacking = self.__whiteMoveMatrix[move[1]][move[0]]
                    if attacking == []:
                        self.__blackMoveMatrix[move[1]][move[0]].append(currentKing.get_ID())
                    elif otherKing != "" and otherKing in attacking:
                        attacking.remove(otherKing)

                else:
                    attacking = self.__blackMoveMatrix[move[1]][move[0]]
                    if attacking == []:
                        self.__whiteMoveMatrix[move[1]][move[0]].append(currentKing.get_ID())
                    elif otherKing != "" and otherKing in attacking:
                        attacking.remove(otherKing)

            otherKing = currentKing.get_ID()



        if whiteChecks != []:
            for place in self.iterate_board():
                X, Y, *rest = place

                hasKing = "Kin_B" in self.__blackMoveMatrix[Y][X]

                if not self.__blocks_check(whiteChecks, (X, Y)):
                    self.__blackMoveMatrix[Y][X] = [] if not hasKing else ["Kin_B"]
        elif blackChecks != []:
            for place in self.iterate_board():
                X, Y, *rest = place

                hasKing = "Kin_W" in self.__whiteMoveMatrix[Y][X]

                if not self.__blocks_check(blackChecks, (X, Y)):
                    self.__whiteMoveMatrix[Y][X] = [] if not hasKing else ["Kin_W"]




    def debug_print_movementMatrix(self):
        print("czarne:")

        for x in range(self.height):
            print(self.__blackMoveMatrix[x])

        print("biale:")
        for x in range(self.height):
            print(self.__whiteMoveMatrix[x])




        

if __name__ == "__main__":
    board = Board(8, 8)
    board.set_piece(3, 3, Knight(True))
    # board.set_piece(4, 0, Rook(True))
    #
    # board.set_piece(2, 1, Rook(False))
    # board.set_piece(7, 2, Rook(False))
    # board.set_piece(7, 3, Rook(False))
    # board.set_piece(7, 4, Rook(False))

    board.make_movement_matrix()

    board.debug_print_movementMatrix()
    board.display_pieces()
    
    # for i in range(8):
    #     board.set_piece(i, 1, Pawn())
    #
    # board.display()
    # print()
    # saved_state = board.export_to_json()
    # save_to_json(saved_state, "boards" + os.sep + "board_state.json")
    # print()
    # board.reset_board()
    # board.display()
    # board.import_from_json(board.export_to_json())
    # board.display()