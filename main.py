import pygame
import copy
import sys

from source.menu.play_submenu.player_selection import PlayerSelection
from source.menu.logo import Logo
from source.menu.menu_background import MenuBackground
from source.menu.main_buttons import MainButtons
from source.menu.play_submenu.players_startup import PlayersStartup

from source.game_logic.game_control import GameControl

from source.board.board import Board
from source.board.piece import *
from source.board.board_json import *
from source.board.board_view import BoardView
from source.menu.choose_board_submenu.choose_board_to_play import ChoosingBoardToPlay
from source.board.square import *

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

    # Logic for moving main menu buttons off-screen and back
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

    # Choose board to play sub-sub-menu
    choose_to_play_pos = SCREEN_WIDTH/2
    choose_to_play_destination_offscreen = int(SCREEN_WIDTH*1.5)
    CHOOSE_BOARD_TO_PLAY = ChoosingBoardToPlay(position=(choose_to_play_destination_offscreen, SCREEN_HEIGHT/2), 
                                               screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT)
    render_choose_to_play = False

    while is_running:
        SCREEN.blit(BG, (0, 0))

        MOUSE_POS = pygame.mouse.get_pos()
        TIME_DELTA = CLOCK.tick(60) / 1000.0
        time = time + TIME_DELTA

        if time < 0:
            time = 0

        MENU_BG.update(SCREEN)
        LOGO.update(SCREEN, time, MOUSE_POS)

        if render_play_menu or PLAY_MENU.is_moving:
            PLAY_MENU.update(SCREEN, time, TIME_DELTA, MOUSE_POS)
        if render_main_menu or MAIN_BTNS.is_moving:
            MAIN_BTNS.update(SCREEN, time, TIME_DELTA, MOUSE_POS)
        if render_choose_to_play or CHOOSE_BOARD_TO_PLAY.is_moving:
            CHOOSE_BOARD_TO_PLAY.update(SCREEN, time, TIME_DELTA, MOUSE_POS)

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
                        if (play_menu_button == 6
                            and not CHOOSE_BOARD_TO_PLAY.is_moving
                            and not PLAY_MENU.is_moving):
                            PLAY_MENU.move(-play_destination_offscreen + SCREEN_WIDTH/2)
                            render_play_menu = False
                            render_choose_to_play = True
                            CHOOSE_BOARD_TO_PLAY.move(choose_to_play_pos)

                if render_choose_to_play:
                    choose_to_play_button = CHOOSE_BOARD_TO_PLAY.checkForInput(MOUSE_POS)
                    if choose_to_play_button:
                        if (choose_to_play_button == 1
                            and not PLAY_MENU.is_moving
                            and not CHOOSE_BOARD_TO_PLAY.is_moving):
                            CHOOSE_BOARD_TO_PLAY.move(choose_to_play_destination_offscreen)
                            render_choose_to_play = False
                            render_play_menu = True
                            PLAY_MENU.move(play_pos)
                        else:
                            gameScreen(choose_to_play_button, 
                                       PLAY_MENU.getCurrentPlayers(), 
                                       PLAY_MENU.getColors(), time)

            if event.type == pygame.KEYDOWN:
                PLAY_MENU.input(event)
            
        pygame.display.update()

    pygame.quit()
    sys.exit()

def gameScreen(currentBoard: Board, players: tuple[str, str], colors: tuple[str, str], time: float):
    pygame.display.set_caption("Szachmider - Gra")
    MENU_BG = MenuBackground(SCREEN_WIDTH, SCREEN_HEIGHT)

    is_running = True
    time = time

    BOARD_VIEW = BoardView(copy.deepcopy(currentBoard), SCREEN_WIDTH, SCREEN_HEIGHT)
    GAME_LOGIC = GameControl(BOARD_VIEW)

    while is_running:
        SCREEN.blit(BG, (0, 0))

        MOUSE_POS = pygame.mouse.get_pos()
        TIME_DELTA = CLOCK.tick(60) / 1000.0
        time = time + TIME_DELTA

        if time < 0:
            time = 0

        MENU_BG.update(SCREEN)
        GAME_LOGIC.display(SCREEN, time)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:   
                is_running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board_input = GAME_LOGIC.checkForInput(MOUSE_POS)
        
        pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    mainMenu()