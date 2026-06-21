from source.gui.button import Button
import pygame


class SizeSelector:
    def __init__(self, xPos, yPos, r = 0, title=""):
        self.xPos = xPos
        self.yPos = yPos


        self.titleDisplay = Button(pos=(self.xPos, self.yPos-60), text=title,
                                       imgNormal=pygame.image.load("assets/buttons/BTN_gray_squished.png").convert_alpha(),
                                       imgHover=pygame.image.load("assets/buttons/BTN_gray_squished.png").convert_alpha(),
                                       r =r + 2)


        if self.titleDisplay.text == "":
            self.titleDisplay.alpha = 0
            self.titleDisplay.newAlpha = 0

        self.BTN_UP = Button(pos=(self.xPos, self.yPos), text="",
                             imgNormal=pygame.image.load("assets/buttons/BTN_small_arrow_up.png").convert_alpha(),
                             imgHover=pygame.image.load("assets/buttons/BTN_small_arrow_up_hover.png").convert_alpha(),
                             r =r + 1)


        self.BTN_SIZE_DISPLAY = Button(pos=(self.xPos, self.yPos+60), text="8",
                                       imgNormal=pygame.image.load("assets/buttons/BTN_gray_field.png").convert_alpha(),
                                       imgHover=pygame.image.load("assets/buttons/BTN_gray_field.png").convert_alpha(),
                                       r =r + 2)


        self.BTN_DOWN = Button(pos=(self.xPos, self.yPos+120), text="",
                               imgNormal=pygame.image.load("assets/buttons/BTN_small_arrow_down.png").convert_alpha(),
                               imgHover=pygame.image.load("assets/buttons/BTN_small_arrow_down_hover.png").convert_alpha(),
                               r =r + 3)


        self.currentSizeChoice = 8
        self.upperSizeLimit = 10
        self.lowerSizeLimit = 4

    def update(self, screen, time, time_delta, position):

        for btn in [self.BTN_UP, self.BTN_SIZE_DISPLAY, self.BTN_DOWN, self.titleDisplay]:
            btn.hover(position)
            btn.update(screen, time, time_delta)

    def get_current_choise(self):
        return self.currentSizeChoice

    def check_for_input(self, position):
        i = 1

        for btn in [self.BTN_UP, self.BTN_DOWN]:
            if btn.check_for_input(position):
                if i == 1:
                    self.currentSizeChoice = min(self.currentSizeChoice+1, self.upperSizeLimit)
                elif i == 2:
                    self.currentSizeChoice = max(self.currentSizeChoice-1, self.lowerSizeLimit)
                self.BTN_SIZE_DISPLAY.text = f"{self.currentSizeChoice}"
                return i
            i += 1
        return 0


    def set_alpha(self, al):
        self.BTN_UP.alpha = al
        self.BTN_UP.newAlpha = al
        self.BTN_DOWN.alpha = al
        self.BTN_DOWN.newAlpha = al
        self.BTN_SIZE_DISPLAY.alpha = al
        self.BTN_SIZE_DISPLAY.newAlpha = al
        if self.titleDisplay.text != "":
            self.titleDisplay.alpha = al
            self.titleDisplay.newAlpha = al

