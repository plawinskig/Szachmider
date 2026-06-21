import pygame
import math

class MenuBackground():
    def __init__(self, screenW, screenH):
        self.screenW = screenW
        self.screenH = screenH
        self.bgImg = pygame.image.load('assets/backgrounds/BG_menu.png').convert_alpha()
        self.backgroundW = self.bgImg.get_width()
        self.tiles = math.ceil(self.screenW / self.backgroundW) + 2

        self.bgVignette = pygame.image.load('assets/backgrounds/BG_vignette.png').convert_alpha()
        self.bgVignette = pygame.transform.scale(self.bgVignette, (self.screenW * 1.2, self.screenH * 1.2))
        self.bgVignetteRect = self.bgVignette.get_rect(center=(self.screenW / 2, self.screenH / 2))

        self.scroll = 0

    def update(self, screen):
        i = 0
        while i < self.tiles:
            screen.blit(self.bgImg, (self.backgroundW * i + self.scroll, -30))
            i += 1

        self.scroll -= 0.25

        if abs(self.scroll) > self.backgroundW:
            self.scroll = 0

        screen.blit(self.bgVignette, self.bgVignetteRect)