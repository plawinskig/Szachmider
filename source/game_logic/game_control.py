import pygame
from pygame import Surface

from source.board.board_view import BoardView
from source.board.board import Board
from source.board.piece import *


class GameControl():
    def __init__(self, board_view: BoardView):
        self.board_view = board_view
        self.board = board_view.board

        self.current_turn = 0
        self.is_white_turn = True

        self.current_piece: Piece = None
        self.current_piece_pos: tuple[int, int] = None
        self.current_legal_moves = None
        self.game_ended: bool = False
        
        self.movesTowardDrawCounter = 0
    

    def display(self, screen: Surface, time):
        self.board_view.display(screen, time, 
                                possible_moves=self.current_legal_moves, piece_pos=self.current_piece_pos)

    def checkForInput(self, mouse_pos):
        board_pos = self.board_view.getBoardCoords(mouse_pos)

        if board_pos:
            if self.current_piece and board_pos in self.current_legal_moves:
                self.board.execute_move(self.current_piece.get_ID(), *board_pos)
                self.current_turn += 1
                self.is_white_turn = not self.is_white_turn
                self.current_piece = None
                self.board.make_movement_matrix()
                if not self.hasLegalMoves():
                    self.game_ended = True
            else:
                current_piece = self.board.get_piece(*board_pos)
                if current_piece:
                    if current_piece.is_black() and not self.is_white_turn:
                        self.current_piece = current_piece
                        self.current_piece_pos = board_pos
                    elif not current_piece.is_black() and self.is_white_turn:
                        self.current_piece = current_piece
                        self.current_piece_pos = board_pos
                    else:
                        self.current_piece = None
                else:
                    self.current_piece = None
        else:
            self.current_piece = None
        
        if self.current_piece:
            self.current_legal_moves = self.board.get_available_moves(self.current_piece.get_ID())
        else:
            self.current_piece_pos = None
            self.current_legal_moves = None

    def hasLegalMoves(self):
        return self.board.does_color_have_any_moves(not self.is_white_turn)