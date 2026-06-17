import os
import types
from typing import Optional

from piece import *
from source.board.square import Square
from square import *
from board_json import save_to_json



class Board:
    def __init__(self, width: int, height: int):
        if width < 4 or height < 4:
            raise ValueError("Board dimensions must be at least 4x4")
        if width > 10 or height > 10:
            raise ValueError("Board dimensions must not exceed 10x10")
        self.width = width
        self.height = height
        self.reset_board()

        self.__whiteMoveMatrix = [[[] for _ in range(self.width)] for _ in range(self.height)]
        self.__blackMoveMatrix = [[[] for _ in range(self.width)] for _ in range(self.height)]

        self.__takenBlack = []
        self.__takenWhite = []
        
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
        self.set_piece(from_x, from_y, None)
        piece.inc_move_counter()

    def move_and_take(self, from_x: int, from_y: int, to_x: int, to_y: int):
        piece = self.get_piece(from_x, from_y)
        taken = self.get_piece(to_x, to_y)

        if piece is None:
            raise ValueError("No piece at the source square")

        if taken.is_black():
            self.__takenBlack.append(taken)
        else:
            self.__takenWhite.append(taken)

        if not self.is_valid_move(from_x, from_y, to_x, to_y):
            raise ValueError("Invalid move")

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

    def display_pieces(self):
        for row in self.board:
            print(" ".join(str(square.piece) for square in row))
    
    def export_to_json(self) -> dict:
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

            for moveIter in currentPiece.moveIterators:
                moveInstance = iter(moveIter)(boardX, boardY)

                encounteredPieces = []
                foundKing = False
                kingLocation = None
                finishedOnKing = False

                plausibleMoves = [] # legalne ruchy iteratora
                canGoFurther = True
                theoriticalMoves = [] # wszystkie ruchy iteratora - do tworzenia oraniczeń

                for move in moveInstance:
                    if (move[0] < 0 or move[0] >= self.width or move[1] < 0 or move[1] >= self.height) and not moveInstance.is_finite():
                        break
                    elif (move[0] < 0 or move[0] >= self.width or move[1] < 0 or move[1] >= self.height) and moveInstance.is_finite():
                        continue

                    nextSquare = self.get_square(move[0], move[1])
                    nextPiece = self.get_piece(move[0], move[1])
                    # print(nextPiece, move)

                    if nextPiece != None:
                        if moveIter.can_take() and nextSquare.get_code() != "Shl" and currentSquare.get_code() != "Hrt" and nextPiece.is_black() != currentPiece.is_black():
                            theoriticalMoves.append(move)
                            if canGoFurther: plausibleMoves.append((move, lambda : self.move_and_take(boardX, boardY, *move)))
                            if not foundKing: encounteredPieces.append(nextPiece)
                            if isinstance(nextPiece, King):
                                foundKing = True
                                kingLocation = move
                                finishedOnKing = True

                        canGoFurther = moveIter.jumps_over() or nextSquare.get_code() == "Grs"
                    else:
                        if moveInstance.can_move():
                            if not foundKing: theoriticalMoves.append(move)
                            if finishedOnKing:
                                if currentPiece.is_black():
                                    additionalBlackChecks.append(move)
                                else:
                                    additionalWhiteChecks.append(move)
                                finishedOnKing = False

                            if canGoFurther: plausibleMoves.append((move, lambda : self.move_piece(boardX, boardY, *move)))

                if finishedOnKing:
                    try:
                        move = next(moveInstance)
                        print(currentPiece.get_ID(), move)
                        if currentPiece.is_black():
                            additionalBlackChecks.append(move)
                        else:
                            additionalWhiteChecks.append(move)
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
                    if currentPiece.is_black():
                        blackChecks.append(theoriticalMoves if not moveInstance.jumps_over() else [kingLocation, (boardX, boardY)])
                    else:
                        whiteChecks.append(theoriticalMoves if not moveInstance.jumps_over() else [kingLocation, (boardX, boardY)])



            if currentSquare.get_code() == "Tel":
                teleLoc = currentSquare.get_tele_location()
                currentPiece.add_possible_moves([(
                    teleLoc,
                    lambda : (self.move_piece(boardX, boardY, *teleLoc) if self.get_piece(*teleLoc) is None else self.move_and_take(boardX, boardY, *teleLoc)
                ))])

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

    def make_movement_matrix(self):
        self.__whiteMoveMatrix = [[[] for _ in range(self.width)] for _ in range(self.height)]
        self.__blackMoveMatrix = [[[] for _ in range(self.width)] for _ in range(self.height)]


        kings, pieces, blackChecks, whiteChecks, additionalBlackChecks, additionalWhiteChecks = self.__get_piece_moves()
        for p in pieces:
            # p.debug_print_moves()
            for move in p.get_actual_move_list():
                moveLoc = move[0]
                if p.is_black():
                    self.__blackMoveMatrix[moveLoc[1]][moveLoc[0]].append((p.get_ID(), move[1]))
                else:
                    self.__whiteMoveMatrix[moveLoc[1]][moveLoc[0]].append((p.get_ID(), move[1]))

        otherKing = ""
        for k in kings:
            currentKing = self.get_piece(*k)
            kingIter = iter(currentKing.moveIterators[0])(*k)

            attackingMatrix = self.__whiteMoveMatrix if currentKing.is_black() else self.__blackMoveMatrix
            ownMoveMatrix = self.__whiteMoveMatrix if not currentKing.is_black() else self.__blackMoveMatrix
            attackingAdditionalChecks = additionalWhiteChecks if currentKing.is_black() else additionalBlackChecks

            for move in kingIter:
                if move[0] < 0 or move[0] >= self.width or move[1] < 0 or move[1] >= self.height:
                    continue

                otherPiece = self.get_piece(*move)

                attacking = attackingMatrix[move[1]][move[0]]
                if attacking == [] and move not in attackingAdditionalChecks:

                    if otherPiece == None:
                        ownMoveMatrix[move[1]][move[0]].append((currentKing.get_ID(), lambda : self.move_piece(*k, *move)))
                    elif not otherPiece.is_black():
                        ownMoveMatrix[move[1]][move[0]].append((currentKing.get_ID(), lambda : self.move_and_take(*k, *move)))


                elif otherKing != "" and otherKing in map(lambda x: x[0], attacking):
                    attacking.pop(self.__find_specific_in_list(otherKing, lambda x: x[0], attacking))
                elif otherKing != "" and otherKing in map(lambda x: x[0], attacking):
                    attacking.pop(self.__find_specific_in_list(otherKing, lambda x: x[0], attacking))




            otherKing = (currentKing.get_ID(), k)



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

    board.set_piece(2, 2, Pawn(True))
    board.set_piece(3, 3, Pawn(False))

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