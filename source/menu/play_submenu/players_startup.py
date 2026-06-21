import pygame
from source.gui.button import Button
from source.menu.play_submenu.player_selection import PlayerSelection
from source.menu.play_submenu.color_selection import ColorButton

class PlayersStartup:
    def __init__(self, position, playerList, screenWidth):
        self.xPos = position[0]
        self.yPos = position[1]

        self.screenWidth = screenWidth

        self.playerList = playerList

        self.BTN_BACK = Button(pos=(self.xPos, 180), text="",
                               imgNormal=pygame.image.load("assets/buttons/BTN_back.png").convert_alpha(),
                               imgHover=pygame.image.load("assets/buttons/BTN_back_hover.png").convert_alpha(),
                               r = 9)

        self.fstPlayer = PlayerSelection(self.xPos, playerList, r=1, offset=self.screenWidth * -0.25)
        self.scndPlayer = PlayerSelection(self.xPos, playerList, r=5, offset=self.screenWidth * 0.25 + 40)

        self.BTN_FST_COLOR = ColorButton((self.xPos - 100, 254), 1, r=3)
        self.BTN_SCND_COLOR = ColorButton((self.xPos + 100, 254), 2, r=7)

        self.BTN_CHOOSE_BOARD = Button(pos=(self.xPos, 700), text="Wybierz planszę",
                                       imgNormal=pygame.image.load("assets/buttons/BTN_play.png").convert_alpha(),
                                       imgHover=pygame.image.load("assets/buttons/BTN_play_hover.png").convert_alpha(),
                                       r = -1, textHoverColor=pygame.Color("#5ac54f"))
        self.BTN_CHOOSE_BOARD.alpha = 0
        self.BTN_CHOOSE_BOARD.newAlpha = 0

        self.containsEqual = False

        self.xDest = self.xPos
        self.isMoving = False
        self.movingRow = 0
        self.rowDelay = 0
        

    def update(self, screen, time, timeDelta, mousePos):
        if self.isMoving:
            buttonsPos = pygame.math.lerp(self.xPos, self.xDest, timeDelta * 6, True)
            self.xPos = buttonsPos
            row = 0
        i = 0

        # Buttons start moving from the side closer to the direction they are moving <- doesn't work sadly (commented the part that broke)
        # Looks more natural that way
        realButtonsIndex = [0, 2, 3, 5]
        buttons = [self.BTN_BACK, self.fstPlayer, self.BTN_FST_COLOR,
                   self.BTN_SCND_COLOR, self.scndPlayer, self.BTN_CHOOSE_BOARD]
        #if (self.x_dest > self.x_pos):
        #   buttons = buttons[::-1]
        #   realButtonsIndex = [5, 3, 2, 0]

        for btn in buttons:
            # Logic for moving the buttons
            if self.isMoving:
                if row == self.movingRow and not btn.isMoving:
                    if i == realButtonsIndex[0]:
                        btn.move(position=(self.xDest - self.screenWidth * 0.4, btn.yDest))
                    elif i == realButtonsIndex[1]:
                        btn.move(position=(self.xDest - 100, btn.yDest))
                    elif i == realButtonsIndex[2]:
                        btn.move(position=(self.xDest + 100, btn.yDest))
                    elif i == realButtonsIndex[3]:
                        btn.move(position=(self.xDest, btn.yDest))
                    else:
                        btn.move(self.xDest)
                if self.rowDelay >= 0.3:
                    self.movingRow += 1
                    self.rowDelay = 0
                self.rowDelay += timeDelta
                row += 1
            
            if i in realButtonsIndex:
                if (i == realButtonsIndex[3] and self.can_play()):
                    btn.newAlpha = 255
                elif (i == realButtonsIndex[3] and not self.can_play()):
                    btn.newAlpha = 0

                btn.hover(mousePos)
                btn.update(screen, time, timeDelta)
            else:
                btn.update(screen, time, timeDelta, mousePos)
            i += 1
        
        if (self.isMoving and not self.fstPlayer.is_moving
                            and not self.BTN_FST_COLOR.isMoving
                            and not self.BTN_SCND_COLOR.isMoving
                            and not self.scndPlayer.is_moving
                            and not self.BTN_BACK.isMoving):
            self.isMoving = False

    def move(self, xDest):
        self.isMoving = True
        if xDest < 0:
            self.xDest = xDest - 1
        else:
            self.xDest = xDest + 1
        self.movingRow = 0
    
    def check_for_input(self, position):
        if self.fstPlayer.checkForInput(position):
            return 1
        elif self.scndPlayer.checkForInput(position):
            return 2
        # Changing color of one player also changes the color of the other, 
        # so that they are not the same
        elif self.BTN_FST_COLOR.check_for_input(position):
            if self.BTN_FST_COLOR.color == 1:
                self.BTN_SCND_COLOR.color = 2
            elif self.BTN_FST_COLOR.color == 2:
                self.BTN_SCND_COLOR.color = 1
            else:
                self.BTN_SCND_COLOR.color = 3
            self.BTN_FST_COLOR.updateColor()
            self.BTN_SCND_COLOR.updateColor()
            return 3
        elif self.BTN_SCND_COLOR.check_for_input(position):
            if self.BTN_SCND_COLOR.color == 1:
                self.BTN_FST_COLOR.color = 2
            elif self.BTN_SCND_COLOR.color == 2:
                self.BTN_FST_COLOR.color = 1
            else:
                self.BTN_FST_COLOR.color = 3
            self.BTN_SCND_COLOR.updateColor()
            self.BTN_FST_COLOR.updateColor()
            return 4
        elif self.BTN_BACK.check_for_input(position):
            return 5
        elif self.BTN_CHOOSE_BOARD.check_for_input(position):
            return 6
        return 0

    def input(self, event):
        self.fstPlayer.input(event)
        self.scndPlayer.input(event)

    def can_play(self):
        return (self.fstPlayer.getPlayer() != self.scndPlayer.getPlayer()
                and self.fstPlayer.getPlayer().strip() in self.playerList
                and self.scndPlayer.getPlayer().strip() in self.playerList)
    
    def get_current_players(self) -> tuple[str, str]:
        return (self.fstPlayer.getPlayer().strip(), self.scndPlayer.getPlayer().strip())
    
    def get_colors(self) -> tuple[int, int]:
        return (self.BTN_FST_COLOR.color, self.BTN_SCND_COLOR)