import math
import pygame

class Button():
    def __init__(self, pos, text: str, img_normal, img_hover, r: int, 
                 text_hover_color = pygame.Color("#ffffff"), text_basic_color =  pygame.Color("#ffffff"), 
                 font_size = 30, font_offset=(1, -4), right_detection_offset=0):
        self.x_pos = pos[0]
        self.y_pos = pos[1]

        # Mainly for text fields, 
        # determines how much pixels from the right edge of the button the input detection should end
        self.right_detection_offset = right_detection_offset

        self.img_normal = img_normal
        self.img_hover = img_hover
        self.r = r  # Random number for floating animation

        self.text = text
        self.font = pygame.font.Font("assets/fonts/born2bsporty-fs.otf", size=font_size)

        self.text_basic_color = text_basic_color
        self.text_hover_color = text_hover_color

        self.current_image = self.img_normal
        self.img_rect = self.current_image.get_rect(center=(self.x_pos, self.y_pos))

        self.width = self.img_normal.get_width()
        self.height = self.img_normal.get_height()
        self.size = 1.0
        self.scale = 1.0

        self.font_x_offset = font_offset[0]
        self.font_y_offset = font_offset[1]
        self.font_text = self.font.render(text=self.text, antialias=False, color=self.text_basic_color)
        self.text_rect = self.font_text.get_rect(center=(self.width / 2 + self.font_x_offset, self.height / 2 + self.font_y_offset))

        self.alpha = 255
        self.new_alpha = 255

        # Moving logic
        self.x_dest = self.x_pos
        self.y_dest = self.y_pos
        self.is_moving = False
        

    def update(self, screen, time, time_delta):
        # Moving logic
        if self.is_moving:
            self.x_pos = pygame.math.lerp(self.x_pos, self.x_dest, time_delta * 6, True)
            self.y_pos = pygame.math.lerp(self.y_pos, self.y_dest, time_delta * 6, True)
        if (self.is_moving and int(self.x_pos) in range(int(self.x_dest) - 2, int(self.x_dest) + 2) 
                            and int(self.y_pos) in range(int(self.y_dest) - 2, int(self.y_dest) + 2)):
            self.is_moving = False

        # Float animation
        angle = math.sin(time * 1.2 + self.r * 0.6)
        new_y_pos = self.y_pos + math.sin(time * 1.5 + self.r * 0.8) * 3
        self.current_image = pygame.transform.rotate(self.current_image, angle)
        self.current_image = pygame.transform.scale(self.current_image, 
                                                    (self.current_image.get_width() * self.scale, 
                                                     self.current_image.get_height() * self.scale))
        self.img_rect = self.current_image.get_rect(center=(self.x_pos, new_y_pos))


        self.font_text = pygame.transform.rotate(self.font_text, angle)
        self.font_text = pygame.transform.scale(self.font_text,
                                                (self.font_text.get_width() * self.scale, 
                                                 self.font_text.get_height() * self.scale))
        self.text_rect = self.font_text.get_rect(center=(self.width / 2 + self.font_x_offset, 
                                                         self.height / 2 + self.font_y_offset))

        # Drawing to screen
        if self.text:
            self.current_image.blit(self.font_text, self.text_rect)
        
        self.alpha = pygame.math.lerp(self.alpha, self.new_alpha, time_delta * 6, True)
        self.current_image.set_alpha(self.alpha)

        screen.blit(self.current_image, self.img_rect)

    def checkForInput(self, position):
        if (position[0] in range(self.img_rect.left, self.img_rect.right - self.right_detection_offset) 
            and position[1] in range(self.img_rect.top, self.img_rect.bottom)
            and self.alpha > 0):
            return True
        return False

    def hover(self, position):
        if (position[0] in range(self.img_rect.left, self.img_rect.right - self.right_detection_offset) 
            and position[1] in range(self.img_rect.top, self.img_rect.bottom)):
            self.current_image = self.img_hover
            self.scale = self.size * 1.05
            self.font_text = self.font.render(text=self.text, 
                                              antialias=False, 
                                              color=self.text_hover_color)
        else:
            self.current_image = self.img_normal
            self.scale = self.size * 1.0
            self.font_text = self.font.render(text=self.text, 
                                              antialias=False, 
                                              color=self.text_basic_color)

    def move(self, position):
        self.x_dest = position[0]
        self.y_dest = position[1]
        self.is_moving = True