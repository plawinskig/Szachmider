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
        self.current_legal_moves = None
    

    def display(self, screen: Surface, time):
        self.board_view.display(screen, time)

    
    def checkForInput(self, mouse_pos):
        board_pos = self.board_view.getBoardCoords(mouse_pos)
        print(board_pos)
        # Choosing a piece
        if board_pos and not self.current_piece:
            current_piece = self.board.get_piece(*board_pos)
            if current_piece:
                if current_piece.is_black() and not self.is_white_turn:
                    self.current_piece = current_piece
                    self.current_legal_moves = self.board.get_available_moves(self.current_piece.get_ID())
                if not current_piece.is_black() and self.is_white_turn:
                    self.current_piece = current_piece
                    self.current_legal_moves = self.board.get_available_moves(self.current_piece.get_ID())
        # Moving a piece (or unselecting it)
        elif board_pos and self.current_piece:
            if board_pos in self.current_legal_moves:
                self.board.execute_move(self.current_piece.get_ID(), *board_pos)
                self.current_turn += 1
                self.is_white_turn = not self.is_white_turn
                #self.board_view.board = self.board
            self.current_piece = None
            self.current_legal_moves = None
        