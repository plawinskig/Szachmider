
import pygame
from source.menu.choose_board_submenu.choose_boards import ChooseBoard
from source.gui.button import Button

class ChoosingBoardToPlay():
    def __init__(self, position, screenWidth, screenHeight):
        self.xPos = position[0]
        self.yPos = position[1]

        self.screenWidth = screenWidth

        self.xDest = self.xPos
        self.isMoving = False
        self.movingRow = 0
        self.rowDelay = 0

        self.BTN_BACK = Button(pos=(self.xPos, 180), text="",
                               imgNormal=pygame.image.load("assets/buttons/BTN_back.png").convert_alpha(),
                               imgHover=pygame.image.load("assets/buttons/BTN_back_hover.png").convert_alpha(),
                               r = 9)
        
        self.boardMenu = ChooseBoard(position, screenWidth, screenHeight)

    def update(self, screen, time, time_delta, mouse_pos):
        if self.isMoving:
            buttonsPos = pygame.math.lerp(self.xPos, self.xDest, time_delta * 6, True)
            self.xPos = buttonsPos
            row = 0
        i = 0

        for btn in [self.BTN_BACK, self.boardMenu]:
            if self.isMoving:
                if row == self.movingRow and not btn.isMoving:
                    if i == 0:
                        btn.move(position=(self.xDest - self.screenWidth * 0.4, btn.yDest))
                    else:
                        btn.move(self.xDest)
                if self.rowDelay >= 0.3:
                    self.movingRow += 1
                    self.rowDelay = 0
                self.rowDelay += time_delta
                row += 1
            
            if i == 0:
                btn.hover(mouse_pos)
                btn.update(screen, time, time_delta)
            else:
                btn.update(screen, time, time_delta, mouse_pos)
            i += 1
        
        if (self.isMoving and not self.BTN_BACK.isMoving
                            and not self.boardMenu.isMoving):
            self.isMoving = False

    def check_for_input(self, position):
        if self.BTN_BACK.check_for_input(position):
            return 1
        else:
            is_board_clicked = self.boardMenu.check_for_input(position)
            if is_board_clicked:
                return self.boardMenu.getRespectiveBoard(is_board_clicked)
        
        return 0

    def move(self, x_dest):
        self.isMoving = True
        self.xDest = x_dest + 1
        self.movingRow = 0

    def setUp(self):
        self.boardMenu.setUp()

