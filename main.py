import pygame
import os
import sys
from source.button import Button

pygame.init()
SCREEN = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Szachmider - Menu")

BG = pygame.Surface((800, 600))
BG.fill(pygame.Color('#f9e6cf'))

def mainMenu():
    is_running = True

    while is_running:
        SCREEN.blit(BG, (0, 0))

        MOUSE_POS = pygame.mouse.get_pos()

        LOGO = pygame.image.load("assets"+os.sep+"logo"+os.sep+"Logo_main.png").convert_alpha()
        LOGO_RECT = LOGO.get_rect(center=(400, 100))
        SCREEN.blit(LOGO, LOGO_RECT)

        BTN_PLAY = Button(pos=(400, 254), img_normal=pygame.image.load("assets/buttons/BTN_play.png").convert_alpha(),
                                    img_hover=pygame.image.load("assets/buttons/BTN_play_hover.png").convert_alpha())

        BTN_STATISTICS = Button(pos=(400, 323), img_normal=pygame.image.load("assets/buttons/BTN_statistics.png").convert_alpha(),
                                    img_hover=pygame.image.load("assets/buttons/BTN_statistics_hover.png").convert_alpha())

        BTN_EDIT = Button(pos=(400, 392), img_normal=pygame.image.load("assets/buttons/BTN_edit.png").convert_alpha(),
                                    img_hover=pygame.image.load("assets/buttons/BTN_edit_hover.png").convert_alpha())

        BTN_EXIT = Button(pos=(400, 461), img_normal=pygame.image.load("assets/buttons/BTN_exit.png").convert_alpha(),
                                    img_hover=pygame.image.load("assets/buttons/BTN_exit_hover.png").convert_alpha())

        for btn in [BTN_PLAY, BTN_STATISTICS, BTN_EDIT, BTN_EXIT]:
            btn.hover(MOUSE_POS)
            btn.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BTN_PLAY.checkForInput(MOUSE_POS):
                    print("Sans Granie")
                if BTN_STATISTICS.checkForInput(MOUSE_POS):
                    print("Statystyki")
                if BTN_EDIT.checkForInput(MOUSE_POS):
                    print("Edit")
                if BTN_EXIT.checkForInput(MOUSE_POS):
                    is_running = False

        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    mainMenu()