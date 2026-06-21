from source.gui.button import Button
import pygame

class TextField(Button):
    def __init__(self, pos, text: str, img_normal, imgHover, r: int,
                 textHoverColor = pygame.Color("#000000"), textBasicColor = pygame.Color("#000000"),
                 max_str_length = 20, rightDetectionOffset=45):
        super().__init__(pos, text, img_normal, imgHover, r, textHoverColor,
                         textBasicColor, rightDetectionOffset=rightDetectionOffset)
        self.is_pressed = False
        self.max_str_length = max_str_length

    def check_for_input(self, position):
        if (position[0] in range(self.imgRect.left, self.imgRect.right - self.rightDetectionOffset)
            and position[1] in range(self.imgRect.top, self.imgRect.bottom)):
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
        self.font_text = self.font.render(text=self.text, antialias=False, color=self.textBasicColor)
        self.text_rect = self.font_text.get_rect(center=(self.width / 2, self.height / 2 - 4))