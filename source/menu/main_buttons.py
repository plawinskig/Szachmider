from source.button import Button
import pygame

class MainButtons():
    def __init__(self, x_pos, screen_width):

        self.screen_width = screen_width
        self.x_pos = x_pos

        self.BTN_PLAY = Button(pos=(self.x_pos, 254),
                            img_normal=pygame.image.load("assets/buttons/BTN_play.png").convert_alpha(),
                            img_hover=pygame.image.load("assets/buttons/BTN_play_hover.png").convert_alpha(), r=1)

        self.BTN_STATISTICS = Button(pos=(self.x_pos, 323),
                            img_normal=pygame.image.load("assets/buttons/BTN_statistics.png").convert_alpha(),
                            img_hover=pygame.image.load("assets/buttons/BTN_statistics_hover.png").convert_alpha(), r=2)

        self.BTN_EDIT = Button(pos=(self.x_pos, 392),
                            img_normal=pygame.image.load("assets/buttons/BTN_edit.png").convert_alpha(),
                            img_hover=pygame.image.load("assets/buttons/BTN_edit_hover.png").convert_alpha(), r=3)

        self.BTN_EXIT = Button(pos=(self.x_pos, 461),
                            img_normal=pygame.image.load("assets/buttons/BTN_exit.png").convert_alpha(),
                            img_hover=pygame.image.load("assets/buttons/BTN_exit_hover.png").convert_alpha(), r=4)

    def update(self, screen, time, position):
        for btn in [self.BTN_PLAY, self.BTN_STATISTICS, self.BTN_EDIT, self.BTN_EXIT]:
            btn.hover(position)
            btn.update(screen, time)

    def checkForInput(self, position):
        i = 1
        for btn in [self.BTN_PLAY, self.BTN_STATISTICS, self.BTN_EDIT, self.BTN_EXIT]:
            if btn.checkForInput(position):
                return i
            i += 1
        return 0

    def move(self, x_pos):
        self.x_pos = x_pos
        for btn in [self.BTN_PLAY, self.BTN_STATISTICS, self.BTN_EDIT, self.BTN_EXIT]:
            btn.move(position=(x_pos, btn.y_pos))