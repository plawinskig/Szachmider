import pygame


from source.gui.button import Button


class PieceSelector:

    def __init__(self, xPos, yPos, r=0):
        self.xPos = xPos
        self.yPos = yPos

        self.__blackButtons = []
        self.__whiteButtons = []
        buttonOffset = 150
        buttonScale = 5

        self.changeColorButton = Button(pos=(self.xPos-buttonOffset, self.yPos), text="",
                                      imgNormal=pygame.image.load(
                                          f"assets/buttons/editor/BTN_switch_piece.png").convert_alpha(),
                                      imgHover=pygame.image.load(
                                          f"assets/buttons/editor/BTN_switch_piece_hover.png").convert_alpha(),
                                      r=r+10)

        rCounter = 1
        for pcType in ["None", "Pawn", "Knight", "Bishop", "Rook", "Queen", "King"]:
            normSprite = pygame.image.load(f"assets/buttons/editor/pieces/{pcType}_dark.png").convert_alpha()
            normSprite = pygame.transform.scale(normSprite, (normSprite.get_width()*buttonScale, normSprite.get_height()*buttonScale))

            hoverSprite = pygame.image.load(f"assets/buttons/editor/pieces/{pcType}_dark.png").convert_alpha()
            hoverSprite = pygame.transform.scale(hoverSprite, (hoverSprite.get_width() * buttonScale, hoverSprite.get_height() * buttonScale))

            self.__blackButtons.append(Button(pos=(self.xPos+(rCounter-1)*buttonOffset, self.yPos), text="",
                                      imgNormal=normSprite,
                                      imgHover=hoverSprite,
                                      r=r + rCounter))
            rCounter += 1


        rCounter = 1
        for pcType in ["None", "Pawn", "Knight", "Bishop", "Rook", "Queen", "King"]:
            normSprite = pygame.image.load(f"assets/buttons/editor/pieces/{pcType}_light.png").convert_alpha()
            normSprite = pygame.transform.scale(normSprite, (normSprite.get_width() * buttonScale, normSprite.get_height() * buttonScale))

            hoverSprite = pygame.image.load(f"assets/buttons/editor/pieces/{pcType}_light.png").convert_alpha()
            hoverSprite = pygame.transform.scale(hoverSprite,(hoverSprite.get_width() * buttonScale, hoverSprite.get_height() * buttonScale))

            self.__whiteButtons.append(Button(pos=(self.xPos + (rCounter - 1) * buttonOffset, self.yPos), text="",
                                              imgNormal=normSprite,
                                              imgHover=hoverSprite,
                                              r=r + rCounter))
            rCounter += 1

        self.__currentSelection = 1
        self.__selectedBlack = True

        otherButtons = self.__blackButtons if not self.__selectedBlack else self.__whiteButtons
        for b in otherButtons:
            b.alpha = 0
            b.newAlpha = 0



    def get_color(self):
        return self.__selectedBlack


    def update(self, screen, time, time_delta, position):

        for btn in self.__blackButtons:
            btn.hover(position)
            btn.update(screen, time, time_delta)

        for btn in self.__whiteButtons:
            btn.hover(position)
            btn.update(screen, time, time_delta)

        self.changeColorButton.hover(position)
        self.changeColorButton.update(screen, time, time_delta)


    def check_for_input(self, position):
        currentButtons = self.__blackButtons if self.__selectedBlack else self.__whiteButtons

        if self.changeColorButton.check_for_input(position):
            self.swap_colors()
            return 0
        for btnIndex in range(len(currentButtons)):
            if currentButtons[btnIndex].check_for_input(position):
                self.__currentSelection = btnIndex
                return 1


        return 0


    def swap_colors(self):
        currentButtons = self.__blackButtons if self.__selectedBlack else self.__whiteButtons
        for b in currentButtons:
            b.newAlpha = 0

        self.__selectedBlack = not self.__selectedBlack
        currentButtons = self.__blackButtons if self.__selectedBlack else self.__whiteButtons
        for b in currentButtons:
            b.newAlpha = 255


    def get_selection(self):
        return self.__currentSelection

    def hide(self):
        currentButtons = self.__blackButtons if self.__selectedBlack else self.__whiteButtons
        for b in currentButtons:
            b.alpha = 0
            b.newAlpha = 0
        self.changeColorButton.alpha = 0
        self.changeColorButton.newAlpha = 0


    def show(self):
        currentButtons = self.__blackButtons if self.__selectedBlack else self.__whiteButtons
        for b in currentButtons:
            b.alpha = 255
            b.newAlpha = 255
        self.changeColorButton.alpha = 255
        self.changeColorButton.newAlpha = 255


