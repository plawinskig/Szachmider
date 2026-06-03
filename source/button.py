import math
import pygame

class Button():
    def __init__(self, pos, img_normal, img_hover, r):
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.img_normal = img_normal
        self.img_hover = img_hover
        self.r = r  # Random number for floating animation
        self.current_image = self.img_normal
        self.rect = self.current_image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen, time):
        # Float animation
        self.current_image = pygame.transform.rotate(self.current_image, math.sin(time * 1.2 + self.r * 0.6))
        self.rect = self.current_image.get_rect(center=(self.x_pos, self.y_pos + math.sin(time * 1.5 + self.r * 0.8) * 3))
        # Drawing to screen
        screen.blit(self.current_image, self.rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def hover(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.current_image = self.img_hover
        else:
            self.current_image = self.img_normal