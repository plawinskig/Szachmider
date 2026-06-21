import pygame

from board.board import Board
from source.gui.button import Button
from source.boardEditor.boardSizeSelector import SizeSelector
from source.boardEditor.squareSelector import SquareSelector
from source.board.square import *
from source.board.piece import *

from source.board.board import Board
from source.board.board_view import BoardView
from source.boardEditor.pieceSelector import PieceSelector

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
        self.pieceSelector = PieceSelector(screenWidth//3, screenHeight-250)

        self.__board = Board(8, 8, "New board")


        self.__boardViewStats = (screenWidth, screenHeight, screenHeight/360)
        self.__boardView = BoardView(self.__board, *self.__boardViewStats)


        self.__currentSelection = ("S", 0)
        self.__squareList = [BasicSquare, GrassSquare, HeartSquare, ShieldSquare, TeleportSquare, None]
        self.__pieceList = [Pawn, Knight, Bishop, Rook, Queen, King]


        self.__isPlacingTele = False
        self.__lastTeleLocation = (0, 0)


        self.__whiteKingExists = False
        self.__blackKingExists = False






    def update(self, screen, time, timeDelta, mousePos):
        selectors = [self.xSizeSel, self.ySizeSel, self.squareSelector, self.pieceSelector]
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
            self.__board = self.__board.get_resized(self.xSizeSel.get_current_choise(), self.__board.height)
            self.__refresh_board_view()
            return 1
        if self.ySizeSel.check_for_input(position):
            self.__board = self.__board.get_resized(self.__board.width, self.ySizeSel.get_current_choise())
            self.__refresh_board_view()
            return 2

        if self.squareSelector.check_for_input(position):
            self.__currentSelection = ("S", self.squareSelector.get_selection())
            return 3

        if self.pieceSelector.check_for_input(position):
            self.__currentSelection = ("P", self.pieceSelector.get_selection())
            return 4

        coords = self.__boardView.getBoardCoords(position)
        if not coords is None:
            if self.__currentSelection[0] == "S":
                self.__set_new_square(*coords)
            elif self.__currentSelection[0] == "P":
                self.__set_new_piece(*coords)

            self.__refresh_board_view()
            return 10

        return 0


    def __refresh_board_view(self):
        self.__boardView = BoardView(self.__board, *self.__boardViewStats)



    def __set_new_square(self, x: int, y: int):
        match self.__currentSelection[1]:
            case 5:
                self.__board.set_square(x, y, None)
            case 4:
                if not self.__isPlacingTele:
                    self.__board.exchange_square(x, y, TeleportSquare((0, 0), None))

                    self.__isPlacingTele = True
                    self.__lastTeleLocation = (x, y)
                    self.squareSelector.set_alpha(0)
                    # self.pieceSelector.hide()

                    self.xSizeSel.set_alpha(0)
                    self.ySizeSel.set_alpha(0)
                elif (x, y) != self.__lastTeleLocation:
                    self.__board.exchange_square(x, y, TeleportSquare(self.__lastTeleLocation, None))
                    self.__board.get_square(*self.__lastTeleLocation).set_tele_location(x, y)

                    self.__isPlacingTele = False
                    self.squareSelector.set_alpha(255)
                    # self.pieceSelector.show()

                    self.xSizeSel.set_alpha(255)
                    self.ySizeSel.set_alpha(255)
            case other:
                self.__board.exchange_square(x, y, self.__squareList[other](None))


    def __set_new_square