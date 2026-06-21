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

        self.__currentSelection = 1




    def update(self, screen, time, time_delta, position):

        for btn in self.__buttons:
            btn.hover(position)
            btn.update(screen, time, time_delta)


    def check_for_input(self, position):
        for btnIndex in range(len(self.__buttons)):
            if self.__buttons[btnIndex].check_for_input(position):
                self.__currentSelection = btnIndex
                return 1
        return 0

    def get_selection(self):
        return self.__currentSelection

    def set_alpha(self, al: int):

        for b in self.__buttons:
            b.alpha = al
            b.newAlpha = al