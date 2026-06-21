import pygame
import os

from source.board.board_view import BoardView
from source.gui.button import Button
from source.board.board import Board
from source.board.board_json import *

class ChooseBoard():
    def __init__(self, position, screenWidth, screenHeight, canAddNew: bool = False):
        self.xPos = position[0]
        self.yPos = position[1]

        self.xDest = self.xPos
        self.yDest = self.yPos

        self.isMoving = False
        self.movingRow = 0
        self.rowDelay = 0

        self.canAddNew = canAddNew

        self.screenWidth = screenWidth
        self.screenHeight = screenHeight

        self.BTN_LEFT = Button(pos=(self.xPos - 475, screenHeight / 2), text="",
                               imgNormal=pygame.image.load("assets/buttons/BTN_arrow_left.png").convert_alpha(),
                               imgHover=pygame.image.load("assets/buttons/BTN_arrow_left_hover.png").convert_alpha(),
                               r = -1)
        self.boardList: list[Board]
        self.boardList = []

        path = "boards"
        for folder in os.scandir(path):
            if folder.is_dir():
                for file in os.scandir(folder):
                    if file.is_file():
                        boardData = load_from_json(file.path)
                        board = Board(5, 5, "template")
                        board.import_from_json(boardData)
                        self.boardList.append(board)

        self.BTN_BOARD_LIST = []
        i = 0
        for board in self.boardList:
            imgNormal=pygame.image.load("assets/buttons/BTN_board_select.png").convert_alpha()
            imgHover=pygame.image.load("assets/buttons/BTN_board_select_hover.png").convert_alpha()

            boardView = BoardView(board, imgNormal.get_width(), imgNormal.get_height(), scale=1)

            boardView.display(imgNormal, 0)
            boardView.display(imgHover, 0)

            button = Button(pos=(self.xPos + 300 * i, screenHeight / 2), text="",
                            imgNormal=imgNormal,
                            imgHover=imgHover,
                            r = i + 1)
            
            self.BTN_BOARD_LIST.append(button)
            i += 1
        
        self.currentListPos = 0
        self.maxListPos = i
        self.move_the_list(0)
        
        # Dummy button for better looking movement of BTN_DOWN, 
        # so it's not moved with the same speed as the player list
        self.BTN_EMPTY = Button(pos=(self.xPos, 0), text="",
                                imgNormal=pygame.image.load("assets/buttons/BTN_nametag.png").convert_alpha(),
                                imgHover=pygame.image.load("assets/buttons/BTN_nametag_hover.png").convert_alpha(),
                                r = 0)
        self.BTN_EMPTY.alpha = 0
        self.BTN_EMPTY.newAlpha = 0

        self.BTN_RIGHT = Button(pos=(self.xPos + 475, screenHeight / 2), text="",
                                imgNormal=pygame.image.load("assets/buttons/BTN_arrow_right.png").convert_alpha(),
                                imgHover=pygame.image.load("assets/buttons/BTN_arrow_right_hover.png").convert_alpha(),
                                r = 1)
        


    def update(self, screen, time, time_delta, mouse_pos):
        if self.isMoving:
            buttonsPos = pygame.math.lerp(self.xPos, self.xDest, time_delta * 6, True)
            self.xPos = buttonsPos
            row = 0
        i = 0
        for btn in [self.BTN_LEFT, self.BTN_EMPTY, self.BTN_RIGHT]:
            # Logic for moving the buttons 
            if self.isMoving:
                if row == self.movingRow and not btn.isMoving:
                    if i == 0:
                        btn.move(position=(self.xDest - 475, btn.yPos))
                    else:
                        btn.move(position=(self.xDest + 475, btn.yPos))
                if self.rowDelay >= 0.3:
                    self.movingRow += 1
                    self.rowDelay = 0
                self.rowDelay += time_delta
                row += 1
            
            btn.hover(mouse_pos)
            btn.update(screen, time, time_delta)
            i += 1

        # Logic for moving the board list
        i = 0
        for btn in self.BTN_BOARD_LIST:
            if self.isMoving and not btn.isMoving and self.movingRow > 1:
                btn.move(position=(self.xDest + 300 * (i - self.currentListPos), btn.yDest))
            i += 1
            
            btn.hover(mouse_pos)
            btn.update(screen, time, time_delta)

        if (self.isMoving and not self.BTN_LEFT.isMoving
                            and not self.BTN_EMPTY.isMoving
                            and not self.BTN_RIGHT.isMoving):
            self.isMoving = False


    def move_the_list(self, direction: int):
        if ((direction + self.currentListPos) >= 0
            and (direction + self.currentListPos) < self.maxListPos):
            #and not self.BTN_BOARD_LIST[self.current_list_pos].is_moving):
            self.currentListPos = direction + self.currentListPos
            i = 0
            for btn in self.BTN_BOARD_LIST:
                btn.move(position=(btn.xDest + 300 * (-1 * direction), btn.yDest))
                if i <= self.currentListPos - 2 or i >= self.currentListPos + 2:
                    btn.newAlpha = 0
                    if direction == 0:
                        btn.alpha = 0
                else:
                    btn.newAlpha = 255
                    if direction == 0:
                        btn.alpha = 255
                i += 1

    def check_for_input(self, position):
        i = 1
        for btn in [self.BTN_LEFT, self.BTN_RIGHT]:
            if btn.check_for_input(position):
                if i == 1:
                    self.move_the_list(-1)
                elif i == 2:
                    self.move_the_list(1)
                return i
            i += 1
        
        for btn in self.BTN_BOARD_LIST:
            if btn.check_for_input(position):
                return i
            i += 1
        return 0

    def move(self, x_dest):
        self.isMoving = True
        self.xDest = x_dest + 1
        self.movingRow = 0

    def getRespectiveBoard(self, index) -> Board:
        if index >= 3:
            return self.boardList[index - 3]
        return 0