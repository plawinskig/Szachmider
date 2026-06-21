import pygame
from source.gui.button import Button

class SquareSelector:
    def __init__(self, xPos, yPos, r=0):
        self.xPos = xPos
        self.yPos = yPos
        rCounter = 1
        self.__buttons = []
        buttonOffset = 160
        for sqType in ["default", "grass", "heart", "shield", "teleport", "none"]:
            self.__buttons.append(Button(pos=(self.xPos+(rCounter-1)*buttonOffset, self.yPos), text="",
                                      imgNormal=pygame.image.load(
                                          f"assets/buttons/editor/BTN_{sqType}_square.png").convert_alpha(),
                                      imgHover=pygame.image.load(
                                          f"assets/buttons/editor/BTN_{sqType}_square.png").convert_alpha(),
                                      r=r + rCounter))
            rCounter += 1

        self.__currentSelection = 0


    def update(self, screen, time, time_delta, position):

        for btn in self.__buttons:
            btn.hover(position)
            btn.update(screen, time, time_delta)


    def check_for_input(self, position):


        for btnIndex in range(len(self.__buttons)):
            if self.__buttons[btnIndex].check_for_input(position):
                self.__currentSelection = btnIndex
                return btnIndex
        return self.__currentSelection