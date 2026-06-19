import os
import types
from typing import Optional

from source.board.piece import *
from source.board.square import *
from board_json import save_to_json

from source.board.obj_mapping import SQUARE_MAP, PIECE_MAP



class Board:
    def __init__(self, width: int, height: int):
        if width < 4 or height < 4:
            raise ValueError("Board dimensions must be at least 4x4")
        if width > 10 or height > 10:
            raise ValueError("Board dimensions must not exceed 10x10")
            
        self._width = width
        self._height = height
        # self._last_move: Optional[tuple[Piece, Move]] = None
        self._board: list[list[Square]] = []
        
        self.reset_board()

        self.__whiteMoveMatrix = [[[] for _ in range(self.width)] for _ in range(self.height)]
        self.__blackMoveMatrix = [[[] for _ in range(self.width)] for _ in range(self.height)]

        self.__takenBlack = []
        self.__takenWhite = []
        
    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    # @property
    # def last_move(self) -> Optional[tuple[Piece, Move]]:
    #     return self._last_move
    #
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
    
    # def is_valid_move(self, from_x: int, from_y: int, to_x: int, to_y: int) -> bool:
    #     if not (self.is_valid_position(from_x, from_y) and self.is_valid_position(to_x, to_y)):
    #         return False
    
    #     if from_x == to_x and from_y == to_y:
    #         return False
    
    #     moving_piece = self.get_piece(from_x, from_y)
    #     if moving_piece is None:
    #         return False
    
    #     target_piece = self.get_piece(to_x, to_y)
    #     if target_piece is not None and target_piece.is_black() == moving_piece.is_black():
    #         return False
    
    #     # if not moving_piece.can_move(self, move):
    #     #     return False
    
    #     return True
    
    def move_piece(self, from_x: int, from_y: int, to_x: int, to_y: int):
        moving_piece = self.get_piece(from_x, from_y)
        
        if moving_piece is None:
            raise ValueError("No piece at the source square")
        
        # if not self.is_valid_move(move):
        #     raise ValueError("Invalid move")
        
        self.set_piece(to_x, to_y, moving_piece)
        self.set_piece(from_x, from_y, None)
        moving_piece.inc_move_counter()

    def move_and_take(self, from_x: int, from_y: int, to_x: int, to_y: int):
        piece = self.get_piece(from_x, from_y)
        taken = self.get_piece(to_x, to_y)

        if piece is None:
            raise ValueError("No piece at the source square")

        if taken:
            if taken.is_black():
                self.__takenBlack.append(taken)
            else:
                self.__takenWhite.append(taken)

        # if not self.is_valid_move(from_x, from_y, to_x, to_y):
        #     raise ValueError("Invalid move")

        self.set_piece(to_x, to_y, piece)
        self.set_piece(from_x, from_y, None)
        piece.inc_move_counter()

    def take_piece(self, X: int, Y: int):
        taken = self.get_piece(X, Y)

        if taken is None:
            raise ValueError("No piece at the source square")

        if taken.is_black():
            self.__takenBlack.append(taken)
        else:
            self.__takenWhite.append(taken)

        self.set_piece(X, Y, None)

   
    
    def display(self):
        for row in self._board:
            print(" ".join(str(square) for square in row))

    def display_pieces(self):
        for row in self.board:
            print(" ".join(str(square.piece) for square in row))
    
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
    
    def reset_board(self):
        self.board = [[BasicSquare() for _ in range(self.width)] for _ in range(self.height)]


    def iterate_board(self):
        for boardY in range(self.height):
            for boardX in range(self.width):
                yield (boardX, boardY, self.get_square(boardX, boardY), self.get_piece(boardX, boardY))



    # abandon all hope ye who enter here
    def __get_piece_moves(self):
        kings = [] # kings to evaluate later
        pieces = [] # all pieces for ease of making the matrices
        # existings checks iterators
        whiteChecks = []
        blackChecks = []
        # additional moves that are checks but are in current setting unachievable moves (i.e. right behind a king when hes attacked by a rook or pawn attack)
        additionalBlackChecks = []
        additionalWhiteChecks = []

        for place in self.iterate_board():
            boardX, boardY, currentSquare, currentPiece = place
            if  currentPiece == None:
                continue

            if isinstance(currentPiece, King): # król jest ewaluowany na końcu żeby nie wszedł w szacha
                kings.append((boardX, boardY))
                continue

            currentPiece.clear_possible_moves()

            pieces.append(currentPiece)

            currentAdditionalChecks = additionalBlackChecks if currentPiece.is_black() else additionalWhiteChecks
            currentChecks = blackChecks if currentPiece.is_black() else whiteChecks


            for moveIter in currentPiece.moveIterators:
                moveInstance = iter(moveIter)(boardX, boardY)

                encounteredPieces = []
                foundKing = False
                kingLocation = None
                finishedOnKing = False

                plausibleMoves = [] # legalne ruchy iteratora
                canGoFurther = True
                theoriticalMoves = [] # wszystkie ruchy iteratora - do tworzenia ograniczeń

                for move in moveInstance:
                    if (move[0] < 0 or move[0] >= self.width or move[1] < 0 or move[1] >= self.height) and not moveInstance.is_finite():
                        break
                    elif (move[0] < 0 or move[0] >= self.width or move[1] < 0 or move[1] >= self.height) and moveInstance.is_finite():
                        continue

                    nextSquare = self.get_square(move[0], move[1])
                    if nextSquare is None:
                        if moveInstance.jumps_over():
                            continue
                        else:
                            break

                    nextPiece = self.get_piece(move[0], move[1])
                    # print(nextPiece, move)

                    if nextPiece != None:

                        if moveIter.can_take() and nextSquare.get_code() != "Shl" and currentSquare.get_code() != "Hrt" and nextPiece.is_black() != currentPiece.is_black():
                            theoriticalMoves.append(move)
                            if canGoFurther: plausibleMoves.append((move, lambda : self.move_and_take(boardX, boardY, move[0], move[1]), moveInstance.can_take()))
                            if not foundKing: encounteredPieces.append(nextPiece)
                            if isinstance(nextPiece, King):
                                foundKing = True
                                kingLocation = move
                                finishedOnKing = True

                        canGoFurther = moveIter.jumps_over() or nextSquare.get_code() == "Grs"
                    else:
                        if moveIter.can_take() and not moveIter.can_move():
                            currentAdditionalChecks.append(move)

                        if moveInstance.can_move():
                            if not foundKing: theoriticalMoves.append(move)
                            if finishedOnKing:

                                currentAdditionalChecks.append(move)

                                finishedOnKing = False
                            if canGoFurther: plausibleMoves.append((move, lambda : self.move_piece(boardX, boardY, move[0], move[1]), moveInstance.can_take()))

                if finishedOnKing:
                    try:
                        move = next(moveInstance)
                        # print(currentPiece.get_ID(), move)
                        if moveInstance.can_take():
                            currentAdditionalChecks.append(move)
                    except StopIteration:
                        pass
                    except:
                        raise RuntimeError


                # print(plausibleMoves)
                currentPiece.add_possible_moves(plausibleMoves)

                if foundKing and len(encounteredPieces) == 2:
                    restricedPiece = encounteredPieces[0]
                    if isinstance(restricedPiece, King): restricedPiece = encounteredPieces[1]
                    theoriticalMoves.append((boardX, boardY))
                    restricedPiece.set_restrictions(theoriticalMoves)
                elif foundKing and len(encounteredPieces) == 1:
                    theoriticalMoves.append((boardX, boardY))
                    currentChecks.append(theoriticalMoves if not moveInstance.jumps_over() else [kingLocation, (boardX, boardY)])


            specialMoves, specialChecks, specialAdditionalChecks = currentPiece.check_special_moves(self, (boardX, boardY))
            currentPiece.add_possible_moves(specialMoves)
            currentChecks.extend(specialChecks)
            currentAdditionalChecks.extend(specialAdditionalChecks)



            # teleporter
            if isinstance(currentSquare, TeleportSquare):
                teleLoc = currentSquare.get_tele_location()
                currentPiece.add_possible_moves([(
                    teleLoc,
                    lambda : (self.move_piece(boardX, boardY, *teleLoc) if self.get_piece(*teleLoc) is None else self.move_and_take(boardX, boardY, *teleLoc)),
                    True
                )])

        return kings, pieces, blackChecks, whiteChecks, additionalBlackChecks, additionalWhiteChecks



    def __blocks_check(self, checks: list[list[tuple[int, int]]], move: tuple[int, int]):
        blocks = False
        for i in checks:
            if move in i:
                blocks = True

        return blocks


    def __find_specific_in_list(self, val, func, l):
        new = list(map(func, l))
        return new.index(val)

    def __find_move_in_moves_list(self, pieceID: str, moves):
        found = None
        for i in moves:
            if i[0] == pieceID:
                found = i

        return found

    def make_movement_matrix(self):
        self.__whiteMoveMatrix = [[[] for _ in range(self.width)] for _ in range(self.height)]
        self.__blackMoveMatrix = [[[] for _ in range(self.width)] for _ in range(self.height)]


        kings, pieces, blackChecks, whiteChecks, additionalBlackChecks, additionalWhiteChecks = self.__get_piece_moves()
        for p in pieces:
            # p.debug_print_moves()

            currentMoveMatrix = self.__blackMoveMatrix if p.is_black() else self.__whiteMoveMatrix

            for move in p.get_actual_move_list():
                moveLoc = move[0]
                currentMoveMatrix[moveLoc[1]][moveLoc[0]].append((p.get_ID(), move[1], move[2]))


        # evaluating kings moves
        otherKing = ""
        for k in kings:
            currentKing = self.get_piece(*k)
            assert isinstance(currentKing, King)
            kingIter = iter(currentKing.moveIterators[0])(*k)

            attackingMatrix = self.__whiteMoveMatrix if currentKing.is_black() else self.__blackMoveMatrix
            ownMoveMatrix = self.__whiteMoveMatrix if not currentKing.is_black() else self.__blackMoveMatrix
            attackingAdditionalChecks = additionalWhiteChecks if currentKing.is_black() else additionalBlackChecks

            for move in kingIter:
                X, Y = move
                if X < 0 or X >= self.width or Y < 0 or Y >= self.height or self.get_square(X, Y) is None:
                    continue

                otherPiece = self.get_piece(*move)

                attacking = [x for x in attackingMatrix[Y][X] if x[2]]
                if attacking == [] and move not in attackingAdditionalChecks:

                    if otherPiece == None:
                        ownMoveMatrix[Y][X].append((currentKing.get_ID(), lambda : self.move_piece(*k, *move), True))
                    elif otherPiece.is_black() != currentKing.is_black():
                        ownMoveMatrix[Y][X].append((currentKing.get_ID(), lambda : self.move_and_take(*k, *move), True))


                elif otherKing != "" and otherKing in map(lambda x: x[0], attacking):
                    attacking.pop(self.__find_specific_in_list(otherKing, lambda x: x[0], attacking))

            for move in currentKing.check_castling(self, k, attackingMatrix):
                ownMoveMatrix[move[0][1]][move[0][0]].append((currentKing.get_ID(), move[1], move[2]))

            otherKing = (currentKing.get_ID(), k)


        # cchecking moves with existing checks to block them
        if whiteChecks != []:
            for place in self.iterate_board():
                X, Y, *rest = place

                kingsMove = self.__find_move_in_moves_list("Kin_B", self.__blackMoveMatrix[Y][X])

                if not self.__blocks_check(whiteChecks, (X, Y)):
                    self.__blackMoveMatrix[Y][X] = [] if kingsMove is None else [kingsMove]
        elif blackChecks != []:
            for place in self.iterate_board():
                X, Y, *rest = place

                kingsMove = self.__find_move_in_moves_list("Kin_W", self.__whiteMoveMatrix[Y][X])

                if not self.__blocks_check(blackChecks, (X, Y)):
                    self.__whiteMoveMatrix[Y][X] = [] if kingsMove is None else [kingsMove]


    def get_available_moves(self, pieceID: str):
        black = pieceID.split("_")[-1] == "B"
        moveMatrix = self.__blackMoveMatrix if black else self.__whiteMoveMatrix
        result = []

        for y in range(self.height):
            for x in range(self.width):
                if self.__find_move_in_moves_list(pieceID, moveMatrix[y][x]):
                    result.append((x, y))


        return result


    def execute_move(self, pieceID: str, X: int, Y: int):
        black = pieceID.split("_")[-1] == "B"
        moveMatrix = self.__blackMoveMatrix if black else self.__whiteMoveMatrix

        moves = moveMatrix[Y][X]
        moves[self.__find_specific_in_list(pieceID, lambda x: x[0], moves)][1]()




    def debug_print_movementMatrix(self):
        print("czarne:")
        for x in range(self.height):
            print([list(map(lambda b: b[0], a)) for a in self.__blackMoveMatrix[x]])

        print("biale:")
        for x in range(self.height):
            print([list(map(lambda b: b[0], a)) for a in self.__whiteMoveMatrix[x]])




        

if __name__ == "__main__":
    board = Board(8, 8)

    # board.set_piece(0, 0, Rook(True))
    # board.set_piece(7, 0, Rook(True))
    # board.set_piece(1, 0, Knight(True))
    # board.set_piece(6, 0, Knight(True))
    # board.set_piece(2, 0, Bishop(True))
    # board.set_piece(5, 0, Bishop(True))
    # board.set_piece(3, 0, King(True))
    # board.set_piece(4, 0, Queen(True))
    #
    # for i in range(8):
    #     board.set_piece(i, 1, Pawn(True))
    #
    # board.set_piece(0, 7, Rook(False))
    # board.set_piece(7, 7, Rook(False))
    # board.set_piece(1, 7, Knight(False))
    # board.set_piece(6, 7, Knight(False))
    # board.set_piece(2, 7, Bishop(False))
    # board.set_piece(5, 7, Bishop(False))
    # board.set_piece(4, 7, King(False))
    # board.set_piece(3, 7, Queen(False))
    #
    # for i in range(8):
    #     board.set_piece(i, 6, Pawn(False))


    
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