import pygame
from pygame import Surface

from source.board.board import Board
from source.board.square import *


class BoardView:
    def __init__(self, board: Board, screen_width, screen_height, scale: int = 3):
        self.board = board

        self.width = board.width
        self.height = board.height

        self.screen_width = screen_width
        self.screen_height = screen_height

        self.x_tile_size = 22 * scale
        self.y_tile_size = 17 * scale

        self.x_scale = 32 * scale
        self.y_scale = 37 * scale

        board_x_size = self.width * self.x_tile_size + 30
        board_y_size = self.height * self.y_tile_size

        self.x_offset = (self.screen_width - board_x_size) / 2
        self.y_offset = (self.screen_height - board_y_size) / 2 



    def get_board_pos_from_mouse(self, mouse_pos: tuple[int, int], perspective_dark: bool = False) -> tuple[int, int] | None:
        mouse_x, mouse_y = mouse_pos

        if mouse_x < self.x_offset or mouse_y < self.y_offset:
            return None

        x = int((mouse_x - self.x_offset) // self.x_tile_size)
        y = int((mouse_y - self.y_offset) // self.y_tile_size)

        if 0 <= x < self.width and 0 <= y < self.height:
            if perspective_dark:
                return (self.width - 1 - x, self.height - 1 - y)
            return (x, y)
            
        return None


    def display(self, screen: Surface, perspective_dark: bool = False):
        self.displayBase(screen, perspective_dark)
        for y in range(self.height):
            true_y = y
            if perspective_dark:
                true_y = self.height - 1 - y
            for section in ["tile", "back", "piece", "front"]:
                for x in range(self.width):
                    true_x = x
                    if perspective_dark:
                        true_x = self.width - 1 - x
                    square = self.board.get_square(true_x, true_y)
                    if square:
                        img = None
                        is_light = True
                        if (x + y) % 2 == 1:
                            is_light = False
                        
                        if section == "tile":
                            if is_light:
                                img = square.img_tile_light
                            else:
                                img = square.img_tile_dark
                        elif section == "back":
                            if is_light:
                                img = square.img_back_light
                            else:
                                img = square.img_back_dark
                        elif section == "piece":
                            img = None
                        elif section == "front":
                            if is_light:
                                img = square.img_front_light
                            else:
                                img = square.img_front_dark
                        if img != None:
                            img = pygame.image.load(img).convert_alpha()
                            img = pygame.transform.scale(img, (self.x_scale, self.y_scale))
                            screen.blit(img, (self.x_offset + x * self.x_tile_size, 
                                                self.y_offset + y * self.y_tile_size))
                    
                                

                

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

                    


