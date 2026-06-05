import pygame
import sys

from source.menu.play_submenu.player_selection import PlayerSelection
from source.menu.logo import Logo
from source.menu.menu_background import MenuBackground
from source.menu.main_buttons import MainButtons

pygame.init()
SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

GAME_ICON = pygame.image.load("assets/logo/Game_icon.png")
pygame.display.set_icon(GAME_ICON)

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

    LOGO = Logo(pos=(SCREEN_WIDTH/2, 100))

    # Logic for moving buttons off-screen and back
    buttons_pos = SCREEN_WIDTH / 2
    buttons_dest_offscreen = -200

    MAIN_BTNS = MainButtons(buttons_pos,SCREEN_WIDTH)

    # Logic for sub-menus
    # Play sub-menu
    play_pos = int(SCREEN_WIDTH / 2)
    play_destination_offscreen = SCREEN_WIDTH * 2

    # TODO: normalne pobieranie listy graczy
    player_list = ["Gracz 1", "Bardzo długi nick", "Limit znaków = 23", "Chyba działa", "Mam nadzieję"]
    PLAY_MENU = PlayerSelection(play_destination_offscreen, player_list)

    while is_running:
        SCREEN.blit(BG, (0, 0))

        MOUSE_POS = pygame.mouse.get_pos()
        TIME_DELTA = CLOCK.tick(60) / 1000.0
        time = time + TIME_DELTA

        if time < 0:
            time = 0

        MENU_BG.update(SCREEN)
        LOGO.update(SCREEN, time, MOUSE_POS)
        MAIN_BTNS.update(SCREEN, time, TIME_DELTA, MOUSE_POS)
        PLAY_MENU.update(SCREEN, time, TIME_DELTA, MOUSE_POS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                menu_button = MAIN_BTNS.checkForInput(MOUSE_POS)
                if menu_button:
                    if menu_button == 1:
                        MAIN_BTNS.move(buttons_dest_offscreen)
                        PLAY_MENU.move(play_pos)
                        print("Grzes granie")
                    elif menu_button == 2:
                        print("Statystyki")
                    elif menu_button == 3:
                        print("Edit")
                    elif menu_button == 4:
                        is_running = False
                play_menu_button = PLAY_MENU.checkForInput(MOUSE_POS)   
            if event.type == pygame.KEYDOWN:
                PLAY_MENU.input(event)
            
        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    mainMenu()