from source.gui.button import Button
import pygame

class TextField(Button):
    def __init__(self, pos, text: str, img_normal, img_hover, r: int, 
                 text_hover_color = pygame.Color("#000000"), text_basic_color = pygame.Color("#000000"),
                   max_str_length = 23):
        super().__init__(pos, text, img_normal, img_hover, r, text_hover_color, text_basic_color)
        self.is_pressed = False
        self.max_str_length = max_str_length

    def checkForInput(self, position):
        if (position[0] in range(self.img_rect.left, self.img_rect.right) 
            and position[1] in range(self.img_rect.top, self.img_rect.bottom)):
            self.is_pressed = True
            return self.is_pressed
        self.is_pressed = False
        return self.is_pressed
    
    def input(self, event):
        if self.is_pressed:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif len(self.text) < self.max_str_length:
                self.text += event.unicode
        self.updateText()
    
    def updateText(self):
        self.font_text = self.font.render(text=self.text, antialias=False, color=self.text_basic_color)
        self.text_rect = self.font_text.get_rect(center=(self.width / 2, self.height / 2 - 4))