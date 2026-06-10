import pygame
from source.gui.button import Button

class ColorButton(Button):
    def __init__(self, pos, starting_color,r: int, 
                 text_hover_color = pygame.Color("#8a4836"), text_basic_color =  pygame.Color("#5d2c28")):
        self.white_img_normal = pygame.image.load("assets/buttons/BTN_light_piece.png").convert_alpha()
        self.white_img_hover = pygame.image.load("assets/buttons/BTN_light_piece_hover.png").convert_alpha()

        self.black_img_normal = pygame.image.load("assets/buttons/BTN_dark_piece.png").convert_alpha()
        self.black_img_hover = pygame.image.load("assets/buttons/BTN_dark_piece_hover.png").convert_alpha()

        self.random_img_normal = pygame.image.load("assets/buttons/BTN_random_piece.png").convert_alpha()
        self.random_img_hover = pygame.image.load("assets/buttons/BTN_random_piece_hover.png").convert_alpha()

        self.img_normal = self.white_img_normal
        self.img_hover = self.white_img_hover

         # 1 - white, 2 - black, 3 - random
        self.starting_color = starting_color
        self.opposite_color = 0
        if starting_color == 1:
            self.opposite_color = 2
        else:
            self.opposite_color = 1
            self.img_normal = self.black_img_normal
            self.img_hover = self.black_img_hover

        self.color = starting_color

        super().__init__(pos, "", self.img_normal, self.img_hover, r, text_hover_color, text_basic_color, 
                         font_size=50, font_offset=(1, -8))
    
    def updateColor(self):
        if self.color == 1:
            self.img_normal = self.white_img_normal
            self.img_hover = self.white_img_hover
            self.text = ""
        elif self.color == 2:
            self.img_normal = self.black_img_normal
            self.img_hover = self.black_img_hover
            self.text = ""
        else:
            self.img_normal = self.random_img_normal
            self.img_hover = self.random_img_hover
            self.text = "?"

    def checkForInput(self, position):
        if (position[0] in range(self.img_rect.left, self.img_rect.right) 
            and position[1] in range(self.img_rect.top, self.img_rect.bottom)
            and self.alpha > 0):
            if self.color == self.starting_color:
                self.color = self.opposite_color
            elif self.color == self.opposite_color:
                self.color = 3
            else:
                self.color = self.starting_color
            self.updateColor()
            return True
        return False

    