from source.gui.button import Button
import pygame

class MainButtons():
    def __init__(self, x_pos, screen_width):

        self.screenWidth = screen_width
        self.xPos = x_pos

        self.xDest = self.xPos
        self.isMoving = False
        self.movingRow = 0
        self.rowDelay = 0

        self.BTN_PLAY = Button(pos=(self.xPos, 254), text="Graj",
                               imgNormal=pygame.image.load("assets/buttons/BTN_play.png").convert_alpha(),
                               imgHover=pygame.image.load("assets/buttons/BTN_play_hover.png").convert_alpha(), r=1,
                               textHoverColor=pygame.Color("#5ac54f"))

        self.BTN_STATISTICS = Button(pos=(self.xPos, 323), text="Statystyki",
                                     imgNormal=pygame.image.load("assets/buttons/BTN_statistics.png").convert_alpha(),
                                     imgHover=pygame.image.load("assets/buttons/BTN_statistics_hover.png").convert_alpha(), r=2,
                                     textHoverColor=pygame.Color("#0098dc"))

        self.BTN_EDIT = Button(pos=(self.xPos, 392), text="Edytor",
                               imgNormal=pygame.image.load("assets/buttons/BTN_edit.png").convert_alpha(),
                               imgHover=pygame.image.load("assets/buttons/BTN_edit_hover.png").convert_alpha(), r=3,
                               textHoverColor=pygame.Color("#0098dc"))

        self.BTN_EXIT = Button(pos=(self.xPos, 461), text="Wyjdź",
                               imgNormal=pygame.image.load("assets/buttons/BTN_exit.png").convert_alpha(),
                               imgHover=pygame.image.load("assets/buttons/BTN_exit_hover.png").convert_alpha(), r=4,
                               textHoverColor=pygame.Color("#c42430"))

    def update(self, screen, time, timeDelta, position):
        if self.isMoving:
            buttonPos = pygame.math.lerp(self.xPos, self.xDest, timeDelta * 6, True)
            self.xPos = buttonPos
            row = 0
        for btn in [self.BTN_PLAY, self.BTN_STATISTICS, self.BTN_EDIT, self.BTN_EXIT]:
            # Logic for moving the buttons 
            if self.isMoving:
                if row == self.movingRow and not btn.isMoving:
                    btn.move(position=(self.xDest, btn.yPos))
                if self.rowDelay >= 0.3:
                    self.movingRow += 1
                    self.rowDelay = 0
                self.rowDelay += timeDelta
                row += 1
            
            btn.hover(position)
            btn.update(screen, time, timeDelta)
        if (self.isMoving and not self.BTN_PLAY.isMoving
                            and not self.BTN_STATISTICS.isMoving
                            and not self.BTN_EDIT.isMoving
                            and not self.BTN_EXIT.isMoving):
            self.isMoving = False

    def check_for_input(self, position):
        i = 1
        for btn in [self.BTN_PLAY, self.BTN_STATISTICS, self.BTN_EDIT, self.BTN_EXIT]:
            if btn.check_for_input(position):
                return i
            i += 1
        return 0

    def move(self, xDest):
        self.isMoving = True
        self.xDest = xDest + 1
        self.movingRow = 0