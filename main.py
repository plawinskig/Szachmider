import pygame
import sys

from source.menu.play_submenu.player_selection import PlayerSelection
from source.menu.logo import Logo
from source.menu.menu_background import MenuBackground
from source.menu.main_buttons import MainButtons
from source.menu.play_submenu.players_startup import PlayersStartup

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
    render_main_menu = True

    # Logic for sub-menus
    # Play sub-menu
    play_pos = int(SCREEN_WIDTH / 2)
    play_destination_offscreen = SCREEN_WIDTH * 1.5

    # TODO: normalne pobieranie listy graczy
    player_list = ["Gracz 1", "Bardzo długi nick", "Limit znaków = 20", "Chyba działa", "Mam nadzieję"]
    PLAY_MENU = PlayersStartup((play_destination_offscreen, SCREEN_HEIGHT // 2), player_list, screen_width=SCREEN_WIDTH)
    render_play_menu = False

    while is_running:
        SCREEN.blit(BG, (0, 0))

        MOUSE_POS = pygame.mouse.get_pos()
        TIME_DELTA = CLOCK.tick(60) / 1000.0
        time = time + TIME_DELTA

        if time < 0:
            time = 0

        MENU_BG.update(SCREEN)
        LOGO.update(SCREEN, time, MOUSE_POS)
        PLAY_MENU.update(SCREEN, time, TIME_DELTA, MOUSE_POS)
        MAIN_BTNS.update(SCREEN, time, TIME_DELTA, MOUSE_POS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if render_main_menu:
                    menu_button = MAIN_BTNS.checkForInput(MOUSE_POS)
                    if menu_button:
                        if (menu_button == 1 
                            and not MAIN_BTNS.is_moving 
                            and not PLAY_MENU.is_moving):
                            MAIN_BTNS.move(buttons_dest_offscreen)
                            render_main_menu = False
                            render_play_menu = True
                            PLAY_MENU.move(play_pos)
                        elif menu_button == 2:
                            print("Statystyki")
                        elif menu_button == 3:
                            print("Edit")
                        elif menu_button == 4:
                            is_running = False
                if render_play_menu:
                    play_menu_button = PLAY_MENU.checkForInput(MOUSE_POS)
                    if play_menu_button:
                        if (play_menu_button == 5 
                            and not MAIN_BTNS.is_moving 
                            and not PLAY_MENU.is_moving):
                            PLAY_MENU.move(play_destination_offscreen)
                            render_play_menu = False
                            render_main_menu = True
                            MAIN_BTNS.move(buttons_pos)
            if event.type == pygame.KEYDOWN:
                PLAY_MENU.input(event)
            
        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    mainMenu()