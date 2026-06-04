import pygame
import math

class MenuBackground():
    def __init__(self, screen_w, screen_h):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.bg_img = pygame.image.load('assets/backgrounds/BG_menu.png').convert_alpha()
        self.background_w = self.bg_img.get_width()
        self.tiles = math.ceil(self.screen_w / self.background_w) + 2

        self.bg_vignette = pygame.image.load('assets/backgrounds/BG_vignette.png').convert_alpha()
        self.bg_vignette = pygame.transform.scale(self.bg_vignette, (self.screen_w * 1.2, self.screen_h * 1.2))
        self.bg_vignette_rect = self.bg_vignette.get_rect(center=(self.screen_w / 2, self.screen_h / 2))

        self.scroll = 0

    def update(self, screen):
        i = 0
        while i < self.tiles:
            screen.blit(self.bg_img, (self.background_w * i + self.scroll, -30))
            i += 1

        self.scroll -= 0.25

        if abs(self.scroll) > self.background_w:
            self.scroll = 0

        screen.blit(self.bg_vignette, self.bg_vignette_rect)