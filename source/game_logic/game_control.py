import pygame
from pygame import Surface

from source.board.board_view import BoardView
from source.board.board import Board
from source.board.piece import *
from source.gui.button import Button

from source.database.datbaseConnector import DatabaseConnector


class GameControl():
    def __init__(self, boardView: BoardView, whitePlayer: str, blackPlayer: str, 
                 screenWidth: int, screenHeight: int, botPlays: bool = False):
        self.boardView = boardView
        self.board: Board = boardView.board

        self._currentTurn = 0
        self.isWhiteTurn = True

        self.botPlays = botPlays

        self.screenWidth = screenWidth
        self.screenHeight = screenHeight

        self._currentPiece: Piece = None
        self._currentPiecePos: tuple[int, int] = None
        self._CurrentLegalMoves = None

        self.gameEnded: bool = False
        
        self._movesToDraw = 50
        self._movesWithoutTaking = 0

        self._whiteCheck: bool = False
        self._blackCheck: bool = False
        
        self._blackPerspective = False

        self.whitePlayer = whitePlayer
        self.BTN_PLAYER_WHITE = Button(pos=(screenWidth/2, screenHeight-50), text=whitePlayer,
                                        imgNormal=pygame.image.load("assets/buttons/BTN_nametag.png").convert_alpha(),
                                        imgHover=pygame.image.load("assets/buttons/BTN_nametag.png").convert_alpha(),
                                        r = 1)
        
        self.blackPlayer = blackPlayer
        self.BTN_PLAYER_BLACK = Button(pos=(screenWidth/2, 50), text=blackPlayer,
                                        imgNormal=pygame.image.load("assets/buttons/BTN_nametag.png").convert_alpha(),
                                        imgHover=pygame.image.load("assets/buttons/BTN_nametag.png").convert_alpha(),
                                        r = 2)
        
        self.BTN_EXIT = Button(pos=(50, 50), text="",
                                        imgNormal=pygame.image.load("assets/buttons/BTN_back.png").convert_alpha(),
                                        imgHover=pygame.image.load("assets/buttons/BTN_back_hover.png").convert_alpha(),
                                        r = 2)
        
        self.BTN_END = Button(pos=(screenWidth/2, screenHeight/2), text="Koniec gry",
                                        imgNormal=pygame.image.load("assets/buttons/BTN_nametag.png").convert_alpha(),
                                        imgHover=pygame.image.load("assets/buttons/BTN_nametag.png").convert_alpha(),
                                        r = 10)

        
    

    def update(self, screen: Surface, time, timeDelta, mouse_pos):
        self.boardView.display(screen, time, perspective_dark=self._blackPerspective,
                                possible_moves=self._CurrentLegalMoves, piece_pos=self._currentPiecePos,
                                isBlackChecked=self._blackCheck, isWhiteChecked=self._whiteCheck,
                                isWhiteTurn=self.isWhiteTurn, isBlackTurn=not self.isWhiteTurn)
        for btn in [self.BTN_PLAYER_WHITE, self.BTN_PLAYER_BLACK, self.BTN_EXIT]:
            btn.hover(mouse_pos)
            btn.update(screen, time, timeDelta)

        if self.gameEnded:
            self.BTN_END.hover(mouse_pos)
            self.BTN_END.update(screen, time, timeDelta)

    def check_for_input(self, mouse_pos):
        if self.BTN_EXIT.check_for_input(mouse_pos):
            if not self.gameEnded:
                DATABASE = DatabaseConnector()
                games_list = DATABASE.get_games(DATABASE.get_player_id(self.whitePlayer),
                                                DATABASE.get_player_id(self.blackPlayer),
                                                DATABASE.get_board_id(self.boardView.board.getFileName()))
                DATABASE.define_winner(games_list[-1], "D")
                del DATABASE
            return -1
        
        boardPos = None
        if not self.gameEnded:
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

                if not self._has_legal_moves() or self._movesToDraw == 0:
                    self.gameEnded = True
                    DATABASE = DatabaseConnector()
                    games_list = DATABASE.get_games(DATABASE.get_player_id(self.whitePlayer),
                                            DATABASE.get_player_id(self.blackPlayer),
                                            DATABASE.get_board_id(self.boardView.board.getFileName()))
                    DATABASE.define_winner(games_list[-1], self._who_won())
                    del DATABASE
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
        return "N"
            
    