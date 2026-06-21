import pygame
import math
from pygame import Surface

from source.board.board import Board
from source.board.square import *


class BoardView:
    def __init__(self, board: Board, screen_width, screen_height, scale: int = 3):
        self.board: Board = board

        self.width = board.width
        self.height = board.height

        self.screen_width = screen_width
        self.screen_height = screen_height
        
        self.scale = scale

        self.x_tile_size = 22 * scale
        self.y_tile_size = 17 * scale

        self.x_scale = 32 * scale
        self.y_scale = 37 * scale

        self.board_x_size = self.width * self.x_tile_size + 10 * scale
        self.board_y_size = self.height * self.y_tile_size + 20 * scale

        self.x_offset = (self.screen_width - self.board_x_size) / 2
        self.y_offset = (self.screen_height - self.board_y_size) / 2 

    def display(self, screen: Surface, time, perspective_dark: bool = False,
                possible_moves = None, piece_pos = (-1, -1), 
                isBlackChecked: bool = False, isWhiteChecked: bool = False,
                isWhiteTurn: bool = True, isBlackTurn: bool = True):
        self.displayBase(screen, perspective_dark)
        for y in range(self.height):
            true_y = y
            if perspective_dark:
                true_y = self.height - 1 - y
            for section in ["tile", "move", "back", "piece", "check", "front"]:
                for x in range(self.width):
                    true_x = x
                    if perspective_dark:
                        true_x = self.width - 1 - x
                    square = self.board.get_square(true_x, true_y)
                    if square:
                        img = None
                        is_light = True
                        if (true_x + true_y) % 2 == 1:
                            is_light = False
                        
                        if section == "tile":
                            if is_light:
                                img = square.img_tile_light
                            else:
                                img = square.img_tile_dark
                        elif section == "move":
                            if square.piece and piece_pos:
                                if true_x == piece_pos[0] and true_y == piece_pos[1]:
                                    img = "assets/squares/SQR_show_selected.png"
                            if possible_moves and (true_x, true_y) in possible_moves:
                                if square.piece:
                                    img = "assets/squares/SQR_show_take.png"
                                else:
                                    img = "assets/squares/SQR_show_move.png"
                        elif section == "back":
                            if is_light:
                                img = square.img_back_light
                            else:
                                img = square.img_back_dark
                        elif section == "piece":
                            if square.piece:
                                img = square.piece._sprite
                        elif section == "check":
                            if square.piece:
                                if ((square.piece.get_code() == "Kin" 
                                    and square.piece.is_black() 
                                    and isBlackChecked) 
                                    or 
                                    (square.piece.get_code() == "Kin" 
                                    and not square.piece.is_black() 
                                    and isWhiteChecked)):
                                    img = "assets/squares/SQR_check_intigator.png"
                        elif section == "front":
                            if is_light:
                                img = square.img_front_light
                            else:
                                img = square.img_front_dark
                            if square.is_special and not square.piece:
                                img = None
                        if img != None:
                            img = pygame.image.load(img).convert_alpha()
                            img = pygame.transform.scale(img, (self.x_scale, self.y_scale))
                            vertical_offset = 0
                            if section in ["back", "piece", "check", "front"]:
                                direction = 1
                                if section == "piece":
                                    direction = -1
                                    vertical_offset = 13 * self.scale
                                    if square.piece.is_black() and not isBlackTurn:
                                        img.set_alpha(175)
                                    if not square.piece.is_black() and not isWhiteTurn:
                                        img.set_alpha(175)
                                if section == "check":
                                    vertical_offset = 40 * self.scale
                                angle = math.sin(time * 1.2 + x + y * 0.3 * direction)
                                img = pygame.transform.rotate(img, angle)
                            screen.blit(img, (self.x_offset + x * self.x_tile_size, 
                                                self.y_offset + y * self.y_tile_size - vertical_offset))
                    
                                

                

    def displayBase(self, screen: Surface, perspective_dark: bool = False):
        img_base = ["assets/squares/SQR_base_01.png",
                    "assets/squares/SQR_base_02.png",
                    "assets/squares/SQR_base_03.png",
                    "assets/squares/SQR_base_04.png"]
        for base in img_base:
            img = pygame.image.load(base).convert_alpha()
            img = pygame.transform.scale(img, (self.x_scale, self.y_scale))
            for y in range(self.height):
                true_y = y
                if perspective_dark:
                    true_y = self.height - 1 - y
                for x in range(self.width):
                    true_x = x
                    if perspective_dark:
                        true_x = self.width - 1 - x
                    square = self.board.get_square(true_x, true_y)
                    if square:
                        screen.blit(img, (self.x_offset + x * self.x_tile_size, 
                                            self.y_offset + y * self.y_tile_size))

    
    def getBoardCoords(self, mouse_pos):
        offset_pos = (mouse_pos[0] - self.x_offset, mouse_pos[1] - self.y_offset)
        # Offseting the board border
        offset_pos = (offset_pos[0] - 5 * self.scale, offset_pos[1] - 5 * self.scale)
        # Changing size
        offset_pos = (offset_pos[0] / self.x_tile_size, offset_pos[1] / self.y_tile_size)

        if offset_pos[0] < 0 or offset_pos[1] < 0:
            return None
        
        offset_pos = (int(offset_pos[0]), int(offset_pos[1]))

        if offset_pos[0] < self.width and offset_pos[1] < self.height:
            return offset_pos
        return None




