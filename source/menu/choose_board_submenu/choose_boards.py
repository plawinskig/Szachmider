import pygame
import os

from source.board.board_view import BoardView
from source.gui.button import Button
from source.board.board import Board
from source.board.board_json import *

class ChooseBoard():
    def __init__(self, position, screen_width, screen_height, can_add_new: bool = False):
        self.x_pos = position[0]
        self.y_pos = position[1]

        self.x_dest = self.x_pos
        self.y_dest = self.y_pos

        self.is_moving = False
        self.moving_row = 0
        self.row_delay = 0

        self.can_add_new = can_add_new

        self.screen_width = screen_width
        self.screen_height = screen_height

        self.BTN_LEFT = Button(pos=(self.screen_width/2-475, screen_height/2), text="",
                            img_normal=pygame.image.load("assets/buttons/BTN_arrow_left.png").convert_alpha(),
                            img_hover=pygame.image.load("assets/buttons/BTN_arrow_left_hover.png").convert_alpha(),
                            r = -1)
        
        self.board_list = []

        path = "boards"
        for folder in os.scandir(path):
            if folder.is_dir():
                for file in os.scandir(folder):
                    if file.is_file():
                        board_data = load_from_json(file.path)
                        board = Board(5, 5)
                        board.import_from_json(board_data)
                        self.board_list.append(board)

        self.BTN_BOARD_LIST = []
        i = 0
        for board in self.board_list:
            img_normal=pygame.image.load("assets/buttons/BTN_board_select.png").convert_alpha()
            img_hover=pygame.image.load("assets/buttons/BTN_board_select_hover.png").convert_alpha()

            board_view = BoardView(board, img_normal.get_width(), img_normal.get_height(), scale=1)

            board_view.display(img_normal, 0)
            board_view.display(img_hover, 0)

            button = Button(pos=(self.screen_width/2 + 300 * i, screen_height/2), text="",
                            img_normal=img_normal,
                            img_hover=img_hover,
                            r = i + 1)
            
            self.BTN_BOARD_LIST.append(button)
            i += 1
        
        self.current_list_pos = 0
        self.max_list_pos = i
        self.moveTheList(0)
        
        # Dummy button for better looking movement of BTN_DOWN, 
        # so it's not moved with the same speed as the player list
        self.BTN_EMPTY = Button(pos=(self.x_pos, 0), text="",
                            img_normal=pygame.image.load("assets/buttons/BTN_nametag.png").convert_alpha(),
                            img_hover=pygame.image.load("assets/buttons/BTN_nametag_hover.png").convert_alpha(),
                            r = 0)
        self.BTN_EMPTY.alpha = 0
        self.BTN_EMPTY.new_alpha = 0

        self.BTN_RIGHT = Button(pos=(self.screen_width/2+475, screen_height/2), text="",
                            img_normal=pygame.image.load("assets/buttons/BTN_arrow_right.png").convert_alpha(),
                            img_hover=pygame.image.load("assets/buttons/BTN_arrow_right_hover.png").convert_alpha(),
                            r = 1)
        


    def update(self, screen, time, time_delta, position):
        if self.is_moving:
            buttons_pos = pygame.math.lerp(self.x_pos, self.x_dest, time_delta * 6, True)
            self.x_pos = buttons_pos
            row = 0
        for btn in [self.BTN_LEFT, self.BTN_EMPTY, self.BTN_RIGHT]:
            # Logic for moving the buttons 
            if self.is_moving:
                if row == self.moving_row and not btn.is_moving:
                    btn.move(position=(self.x_dest, btn.y_pos))
                if self.row_delay >= 0.3:
                    self.moving_row += 1
                    self.row_delay = 0
                self.row_delay += time_delta
                row += 1
            
            btn.hover(position)
            btn.update(screen, time, time_delta)

        # Logic for moving the board list
        i = 0
        for btn in self.BTN_BOARD_LIST:
            if self.is_moving and not btn.is_moving and self.moving_row > 1:
                btn.move(position=(self.x_dest + 475 * (i - self.current_list_pos), btn.y_dest))
            i += 1
            
            btn.hover(position)
            btn.update(screen, time, time_delta)

        if (self.is_moving and not self.BTN_LEFT.is_moving
                            and not self.BTN_EMPTY.is_moving 
                            and not self.BTN_RIGHT.is_moving):
            self.is_moving = False


    def moveTheList(self, direction: int):
        if ((direction + self.current_list_pos) >= 0 
            and (direction + self.current_list_pos) < self.max_list_pos):
            #and not self.BTN_BOARD_LIST[self.current_list_pos].is_moving):
            self.current_list_pos = direction + self.current_list_pos
            i = 0
            for btn in self.BTN_BOARD_LIST:
                btn.move(position=(btn.x_dest + 300 * (-1 * direction), btn.y_dest))
                if i <= self.current_list_pos - 2 or i >= self.current_list_pos + 2:
                    btn.new_alpha = 0
                    if direction == 0:
                        btn.alpha = 0
                elif i == self.current_list_pos - 1 or i >= self.current_list_pos + 1:
                    btn.new_alpha = 127
                    if direction == 0:
                        btn.alpha = 127
                elif i == self.current_list_pos:
                    btn.new_alpha = 255
                    if direction == 0:
                        btn.alpha = 255
                i += 1

    def checkForInput(self, position):
        i = 1
        for btn in [self.BTN_LEFT, self.BTN_RIGHT]:
            if btn.checkForInput(position):
                if i == 1:
                    self.moveTheList(-1)
                elif i == 2:
                    self.moveTheList(1)
                return i
            i += 1
        
        for btn in self.BTN_BOARD_LIST:
            if btn.checkForInput(position):
                return i
            i += 1
        return 0

    def move(self, x_dest):
        self.is_moving = True
        self.x_dest = x_dest + 1
        self.moving_row = 0

    def getRespectiveBoard(self, index):
        return self.board_list[index-3]