import pygame
import sys
from source.button import Button
from source.menu.logo import Logo
from source.menu.menu_background import MenuBackground
from source.menu.main_buttons import MainButtons

pygame.init()
SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

SCREEN_WIDTH = SCREEN.get_width()
SCREEN_HEIGHT = SCREEN.get_height()

BG = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
BG.fill(pygame.Color('#f9e6cf'))

CLOCK = pygame.time.Clock()

def mainMenu():
    pygame.display.set_caption("Szachmider - Menu")
    MENU_BG = MenuBackground(SCREEN_WIDTH, SCREEN_HEIGHT)
    is_running = True
    time = 0.0

    # Logic for moving buttons off-screen and back
    move_buttons = False
    buttons_pos = SCREEN_WIDTH / 2
    buttons_dest = -200

    while is_running:
        SCREEN.blit(BG, (0, 0))

        MOUSE_POS = pygame.mouse.get_pos()
        TIME_DELTA = CLOCK.tick(60) / 1000.0
        time = time + TIME_DELTA

        if time < 0:
            time = 0

        MENU_BG.update(SCREEN)

        LOGO = Logo(pos=(SCREEN_WIDTH/2, 100))
        LOGO.update(SCREEN, time, MOUSE_POS)

        MAIN_BTNS = MainButtons(buttons_pos,SCREEN_WIDTH)
        # Logic for moving buttons off-screen and back
        if move_buttons:
            buttons_pos = pygame.math.lerp(MAIN_BTNS.x_pos, buttons_dest, TIME_DELTA * 4, True)
            MAIN_BTNS.move(buttons_pos)
            if buttons_dest == MAIN_BTNS.x_pos:
                move_buttons = False

        MAIN_BTNS.update(SCREEN, time, MOUSE_POS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                menu_button = MAIN_BTNS.checkForInput(MOUSE_POS)
                if menu_button:
                    if menu_button == 1:
                        move_buttons = True
                        buttons_dest = -200
                        print("Sans granie")
                    elif menu_button == 2:
                        print("Statystyki")
                    elif menu_button == 3:
                        print("Edit")
                    elif menu_button == 4:
                        is_running = False
        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    mainMenu()