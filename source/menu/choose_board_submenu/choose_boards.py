import pygame

from source.gui.button import Button

class ChooseBoard():
    def __init__(self, position, screen_width, screen_height):
        self.x_pos = position[0]
        self.y_pos = position[1]

        self.screen_width = screen_width
        self.screen_height = screen_height

        self.BTN_LEFT = Button(pos=(self.screen_width-100, screen_height/2), text="",
                            img_normal=pygame.image.load("assets/buttons/BTN_arrow_left.png").convert_alpha(),
                            img_hover=pygame.image.load("assets/buttons/BTN_arrow_left_hover.png").convert_alpha(),
                            r = -1)
        
        self.BTN_RIGHT = Button(pos=(self.screen_width+100, screen_height/2), text="",
                            img_normal=pygame.image.load("assets/buttons/BTN_arrow_right.png").convert_alpha(),
                            img_hover=pygame.image.load("assets/buttons/BTN_arrow_right_hover.png").convert_alpha(),
                            r = 1)