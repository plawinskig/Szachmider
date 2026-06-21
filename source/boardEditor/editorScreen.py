import pygame

from source.gui.button import Button
from source.boardEditor.boardSizeSelector import SizeSelector
from source.boardEditor.squareSelector import SquareSelector
from source.board.square import *
from source.board.board import Board
from source.board.board_view import BoardView

class EditorScreen:
    def __init__(self, position, screenWidth, screenHeight):
        self.xPos = position[0]
        self.yPos = position[1]

        self.screenWidth = screenWidth


        self.BTN_BACK = Button(pos=(self.xPos+80, self.yPos+80), text="",
                               imgNormal=pygame.image.load("assets/buttons/BTN_back.png").convert_alpha(),
                               imgHover=pygame.image.load("assets/buttons/BTN_back_hover.png").convert_alpha(),
                               r = 9)

        self.xSizeSel = SizeSelector(screenWidth//10, screenHeight//3, r=1)
        self.ySizeSel = SizeSelector(screenWidth//10+80, screenHeight//3, r=1)

        self.squareSelector = SquareSelector(screenWidth//3, screenHeight-100, r=1)

        self.__board = Board(8, 8, "New board")

        self.__boardView = BoardView(self.__board, screenWidth, screenHeight, screenHeight/360)


        self.__currentSelection = ("S", 0)
        self.__squareList = [BasicSquare, GrassSquare, HeartSquare, ShieldSquare, TeleportSquare, None]





    def update(self, screen, time, timeDelta, mousePos):
        selectors = [self.xSizeSel, self.ySizeSel, self.squareSelector]
        buttons = [self.BTN_BACK]

        for sl in selectors:
            sl.update(screen, time, timeDelta, mousePos)


        for btn in buttons:
            btn.hover(mousePos)
            btn.update(screen, time, timeDelta)

        self.__boardView.display(screen, time)




    def check_for_input(self, position):

        if self.BTN_BACK.check_for_input(position):
            return -1
        if self.xSizeSel.check_for_input(position):
            return 1
        if self.ySizeSel.check_for_input(position):
            return 2
        sel = self.squareSelector.check_for_input(position)
        if sel:
            self.__currentSelection = ("S", sel)
            return 3

        return 0

