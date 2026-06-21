import pygame
from pygame import Surface

from source.board.board_view import BoardView
from source.board.board import Board
from source.board.piece import *


class GameControl():
    def __init__(self, boardView: BoardView, whitePlayer: str, blackPlayer: str):
        self.boardView = boardView
        self.board: Board = boardView.board

        self._currentTurn = 0
        self.isWhiteTurn = True

        self._currentPiece: Piece = None
        self._currentPiecePos: tuple[int, int] = None
        self._CurrentLegalMoves = None

        self.gameEnded: bool = False
        
        self._movesToDraw = 50
        self._movesWithoutTaking = 0

        self._whiteCheck: bool = False
        self._blackCheck: bool = False

        
    

    def display(self, screen: Surface, time):
        self.boardView.display(screen, time, 
                                possible_moves=self._CurrentLegalMoves, piece_pos=self._currentPiecePos,
                                isBlackChecked=self._blackCheck, isWhiteChecked=self._whiteCheck)

    def check_for_input(self, mouse_pos):
        boardPos = self.boardView.getBoardCoords(mouse_pos)

        if boardPos:
            if self._currentPiece and boardPos in self._CurrentLegalMoves:
                # If no piece is taken or no pawn is moved for 50 rounds the game ends in a draw
                if self._is_take(boardPos) or self._currentPiece.get_code() == "Paw":
                    self._movesToDraw = 50
                else:
                    self._movesToDraw -= 1
                
                self.board.execute_move(self._currentPiece.get_ID(), *boardPos)
                self._currentTurn += 1
                self.isWhiteTurn = not self.isWhiteTurn
                self._currentPiece = None
                self.board.make_movement_matrix()    

                self._whiteCheck = self.isWhiteTurn and self._is_in_check()
                self._blackCheck = not self.isWhiteTurn and self._is_in_check()
                print((self._whiteCheck, self._blackCheck))

                if not self._has_legal_moves() or not self._movesToDraw:
                    self.gameEnded = True
            else:
                currentPiece = self.board.get_piece(*boardPos)
                if currentPiece:
                    if currentPiece.is_black() and not self.isWhiteTurn:
                        self._currentPiece = currentPiece
                        self._currentPiecePos = boardPos
                    elif not currentPiece.is_black() and self.isWhiteTurn:
                        self._currentPiece = currentPiece
                        self._currentPiecePos = boardPos
                    else:
                        self._currentPiece = None
                else:
                    self._currentPiece = None
        else:
            self._currentPiece = None
        
        if self._currentPiece:
            self._CurrentLegalMoves = self.board.get_available_moves(self._currentPiece.get_ID())
        else:
            self._currentPiecePos = None
            self._CurrentLegalMoves = None

    def _has_legal_moves(self):
        return self.board.does_color_have_any_moves(not self.isWhiteTurn)
    
    def _is_in_check(self) -> bool:
        return self.board.king_in_check(not self.isWhiteTurn)
    
    def _is_take(self, position: tuple[int, int]) -> bool:
        return True if self.board.get_piece(*position) else False
    
    def _who_won(self):
        if self.gameEnded:
            self.isWhiteTurn = True
            whiteWon = not self._is_in_check() and self._has_legal_moves()
            self.isWhiteTurn = False
            blackWon = not self._is_in_check() and self._has_legal_moves()

            if whiteWon and not blackWon:
                return "W"
            if blackWon and not whiteWon:
                return "B"
            if not whiteWon and not blackWon:
                return "D"
        return None
            
    