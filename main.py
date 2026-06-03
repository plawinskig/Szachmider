import pygame
import sys
from source.button import Button
from source.logo import Logo
from source.menu_background import MenuBackground


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

pygame.init()
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Szachmider - Menu")

BG = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
BG.fill(pygame.Color('#f9e6cf'))

MENU_BG = MenuBackground(SCREEN_WIDTH, SCREEN_HEIGHT)

CLOCK = pygame.time.Clock()

def mainMenu():
    is_running = True
    time = 0.0

    while is_running:
        SCREEN.blit(BG, (0, 0))

        MOUSE_POS = pygame.mouse.get_pos()
        TIME_DELTA = CLOCK.tick(60) / 1000.0
        time = time + TIME_DELTA

        if time < 0:
            time = 0

        MENU_BG.update(SCREEN)

        LOGO = Logo(pos=(SCREEN_WIDTH/2, 100))
        LOGO.update(SCREEN, time)



        BTN_PLAY = Button(pos=(SCREEN_WIDTH/2, 254),
                                img_normal=pygame.image.load("assets/buttons/BTN_play.png").convert_alpha(),
                                img_hover=pygame.image.load("assets/buttons/BTN_play_hover.png").convert_alpha(), r=1)

        BTN_STATISTICS = Button(pos=(SCREEN_WIDTH/2, 323),
                                img_normal=pygame.image.load("assets/buttons/BTN_statistics.png").convert_alpha(),
                                img_hover=pygame.image.load("assets/buttons/BTN_statistics_hover.png").convert_alpha(), r=2)

        BTN_EDIT = Button(pos=(SCREEN_WIDTH/2, 392),
                                img_normal=pygame.image.load("assets/buttons/BTN_edit.png").convert_alpha(),
                                img_hover=pygame.image.load("assets/buttons/BTN_edit_hover.png").convert_alpha(), r=3)

        BTN_EXIT = Button(pos=(SCREEN_WIDTH/2, 461),
                                img_normal=pygame.image.load("assets/buttons/BTN_exit.png").convert_alpha(),
                                img_hover=pygame.image.load("assets/buttons/BTN_exit_hover.png").convert_alpha(), r=4)

        for btn in [BTN_PLAY, BTN_STATISTICS, BTN_EDIT, BTN_EXIT]:
            btn.hover(MOUSE_POS)
            btn.update(SCREEN, time)

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