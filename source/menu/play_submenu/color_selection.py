import pygame
from source.gui.button import Button

class ColorButton(Button):
    def __init__(self, pos, startingColor, r: int,
                 textCoverColor = pygame.Color("#8a4836"), textBasicColor =  pygame.Color("#5d2c28")):
        self.whiteImgNormal = pygame.image.load("assets/buttons/BTN_light_piece.png").convert_alpha()
        self.whiteImgHover = pygame.image.load("assets/buttons/BTN_light_piece_hover.png").convert_alpha()

        self.blackImgNormal = pygame.image.load("assets/buttons/BTN_dark_piece.png").convert_alpha()
        self.blackImgHover = pygame.image.load("assets/buttons/BTN_dark_piece_hover.png").convert_alpha()

        self.randomImgNormal = pygame.image.load("assets/buttons/BTN_random_piece.png").convert_alpha()
        self.randomImgHover = pygame.image.load("assets/buttons/BTN_random_piece_hover.png").convert_alpha()

        self.imgNormal = self.whiteImgNormal
        self.imgHover = self.whiteImgHover

         # 1 - white, 2 - black, 3 - random
        self.startingColor = startingColor
        self.oppositeColor = 0
        if startingColor == 1:
            self.oppositeColor = 2
        else:
            self.oppositeColor = 1
            self.imgNormal = self.blackImgNormal
            self.imgHover = self.blackImgHover

        self.color = startingColor

        super().__init__(pos, "", self.imgNormal, self.imgHover, r, textCoverColor, textBasicColor,
                         fontSize=50, fontOffset=(1, -8))
    
    def updateColor(self):
        if self.color == 1:
            self.imgNormal = self.whiteImgNormal
            self.imgHover = self.whiteImgHover
            self.text = ""
        elif self.color == 2:
            self.imgNormal = self.blackImgNormal
            self.imgHover = self.blackImgHover
            self.text = ""
        else:
            self.imgNormal = self.randomImgNormal
            self.imgHover = self.randomImgHover
            self.text = "?"

    def check_for_input(self, position):
        if (position[0] in range(self.imgRect.left, self.imgRect.right)
            and position[1] in range(self.imgRect.top, self.imgRect.bottom)
            and self.alpha > 0):
            if self.color == self.startingColor:
                self.color = self.oppositeColor
            elif self.color == self.oppositeColor:
                self.color = 3
            else:
                self.color = self.startingColor
            self.updateColor()
            return True
        return False

    