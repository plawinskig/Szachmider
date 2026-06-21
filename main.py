import pygame
import copy
import random
import sys

from source.statistics.statistics_full import Statistics
from source.menu.logo import Logo
from source.menu.menu_background import MenuBackground
from source.menu.main_buttons import MainButtons
from source.menu.play_submenu.players_startup import PlayersStartup

from source.game_logic.game_control import GameControl
from source.bot.random_bot import RandomBot

from source.board.board import Board
from source.board.piece import *
from source.board.board_json import *
from source.board.board_view import BoardView
from source.menu.choose_board_submenu.choose_board_to_play import ChoosingBoardToPlay
from source.board.square import *

from source.boardEditor.editorScreen import EditorScreen

from source.database.datbaseConnector import *

from source.shaders.crt_effect import *

pygame.init()
SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

BOT_PLAYER_NAME = "Random Bot"

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

    DATABASE = DatabaseConnector()
    player_list = DATABASE.get_player_list()
    if BOT_PLAYER_NAME not in player_list:
        DATABASE.add_player(BOT_PLAYER_NAME)
        player_list = DATABASE.get_player_list()
    del DATABASE
    PLAY_MENU = PlayersStartup((play_destination_offscreen, SCREEN_HEIGHT // 2), player_list, screenWidth=SCREEN_WIDTH)
    render_play_menu = False

    # Choose board to play sub-sub-menu
    choose_to_play_pos = SCREEN_WIDTH/2
    choose_to_play_destination_offscreen = int(SCREEN_WIDTH*1.5)
    CHOOSE_BOARD_TO_PLAY = ChoosingBoardToPlay(position=(choose_to_play_destination_offscreen, SCREEN_HEIGHT/2),
                                               screenWidth=SCREEN_WIDTH, screenHeight=SCREEN_HEIGHT)
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

        if render_play_menu or PLAY_MENU.isMoving:
            PLAY_MENU.update(SCREEN, time, TIME_DELTA, MOUSE_POS)
        if render_main_menu or MAIN_BTNS.isMoving:
            MAIN_BTNS.update(SCREEN, time, TIME_DELTA, MOUSE_POS)
        if render_choose_to_play or CHOOSE_BOARD_TO_PLAY.isMoving:
            CHOOSE_BOARD_TO_PLAY.update(SCREEN, time, TIME_DELTA, MOUSE_POS)
        
        apply_crt_effect(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if render_main_menu:
                    menu_button = MAIN_BTNS.check_for_input(MOUSE_POS)
                    if menu_button:
                        if (menu_button == 1 
                            and not MAIN_BTNS.isMoving
                            and not PLAY_MENU.isMoving):
                            MAIN_BTNS.move(buttons_dest_offscreen)
                            render_main_menu = False
                            render_play_menu = True
                            PLAY_MENU.move(play_pos)
                        elif menu_button == 2:
                            statisticsScreen(time)
                        elif (menu_button == 3):
                            editScreen(time)
                        elif menu_button == 4:
                            is_running = False
                
                if render_play_menu:
                    play_menu_button = PLAY_MENU.check_for_input(MOUSE_POS)
                    if play_menu_button:
                        if (play_menu_button == 5 
                            and not MAIN_BTNS.isMoving
                            and not PLAY_MENU.isMoving):
                            PLAY_MENU.move(play_destination_offscreen)
                            render_play_menu = False
                            render_main_menu = True
                            MAIN_BTNS.move(buttons_pos)
                        if (play_menu_button == 6
                            and not CHOOSE_BOARD_TO_PLAY.isMoving
                            and not PLAY_MENU.isMoving):
                            PLAY_MENU.move(-play_destination_offscreen + SCREEN_WIDTH/2)
                            render_play_menu = False
                            render_choose_to_play = True
                            CHOOSE_BOARD_TO_PLAY.move(choose_to_play_pos)

                if render_choose_to_play:
                    choose_to_play_button = CHOOSE_BOARD_TO_PLAY.check_for_input(MOUSE_POS)
                    if choose_to_play_button:
                        if (choose_to_play_button == 1
                            and not PLAY_MENU.isMoving
                            and not CHOOSE_BOARD_TO_PLAY.isMoving):
                            CHOOSE_BOARD_TO_PLAY.move(choose_to_play_destination_offscreen)
                            render_choose_to_play = False
                            render_play_menu = True
                            PLAY_MENU.move(play_pos)
                        elif choose_to_play_button != 1:
                            gameScreen(choose_to_play_button,
                                       PLAY_MENU.get_current_players(),
                                       PLAY_MENU.get_colors(), time)

            if event.type == pygame.KEYDOWN:
                PLAY_MENU.input(event)
            
        pygame.display.update()

    pygame.quit()
    sys.exit()

def gameScreen(currentBoard: Board, players: tuple[str, str], colors: tuple[int, int], time: float):
    pygame.display.set_caption("Szachmider - Gra")
    MENU_BG = MenuBackground(SCREEN_WIDTH, SCREEN_HEIGHT)

    isRunning = True

    # 1 - white, 2 - black, 3 - random
    if colors[0] == 3:
        if random.random() < 0.5:
            colors = (1, 2)
        else:
            colors = (2, 1)

    if colors[0] == 1:
        whitePlayer = players[0]
        blackPlayer = players[1]
    else:
        whitePlayer = players[1]
        blackPlayer = players[0]

    BOARD_VIEW = BoardView(copy.deepcopy(currentBoard), SCREEN_WIDTH, SCREEN_HEIGHT)
    whiteBot = RandomBot(is_black=False) if whitePlayer == BOT_PLAYER_NAME else None
    blackBot = RandomBot(is_black=True) if blackPlayer == BOT_PLAYER_NAME else None
    GAME_LOGIC = GameControl(BOARD_VIEW, whitePlayer, blackPlayer, SCREEN_WIDTH, SCREEN_HEIGHT,
                             whiteBot=whiteBot, blackBot=blackBot)

    DATABASE = DatabaseConnector()
    DATABASE.add_game(DATABASE.get_player_id(whitePlayer),
                    DATABASE.get_player_id(blackPlayer),
                    DATABASE.get_board_id(BOARD_VIEW.board.getFileName()))

    while isRunning:
        SCREEN.blit(BG, (0, 0))

        MOUSE_POS = pygame.mouse.get_pos()
        TIME_DELTA = CLOCK.tick(60) / 1000.0
        time = time + TIME_DELTA

        if time < 0:
            time = 0

        MENU_BG.update(SCREEN)
        GAME_LOGIC.update(SCREEN, time, TIME_DELTA, MOUSE_POS)

        apply_crt_effect(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:   
                isRunning = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board_input = GAME_LOGIC.check_for_input(MOUSE_POS)
                if board_input:
                    if board_input == -1:
                        isRunning = False
        
        pygame.display.update()

def statisticsScreen(time: float):
    pygame.display.set_caption("Szachmider - Statystyki")
    MENU_BG = MenuBackground(SCREEN_WIDTH, SCREEN_HEIGHT)

    isRunning = True

    STATISTICS = Statistics(SCREEN_WIDTH, SCREEN_HEIGHT)

    while isRunning:
        SCREEN.blit(BG, (0, 0))

        MOUSE_POS = pygame.mouse.get_pos()
        TIME_DELTA = CLOCK.tick(60) / 1000.0
        time = time + TIME_DELTA

        if time < 0:
            time = 0

        MENU_BG.update(SCREEN)

        STATISTICS.update(SCREEN, time, TIME_DELTA, MOUSE_POS)

        apply_crt_effect(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:   
                isRunning = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                statistics_button = STATISTICS.check_for_input(MOUSE_POS)
                if statistics_button:
                    if statistics_button == -1:
                        isRunning = False
        
            if event.type == pygame.KEYDOWN:
                STATISTICS.input(event)
        
        pygame.display.update()




def editScreen(time: float):
    pygame.display.set_caption("Szachmider - Edytor")
    MENU_BG = MenuBackground(SCREEN_WIDTH, SCREEN_HEIGHT)

    is_running = True

    EDIT_MENU = EditorScreen((0, 0), SCREEN_WIDTH, SCREEN_HEIGHT)

    while is_running:
        SCREEN.blit(BG, (0, 0))

        MOUSE_POS = pygame.mouse.get_pos()
        TIME_DELTA = CLOCK.tick(60) / 1000.0
        time = time + TIME_DELTA

        if time < 0:
            time = 0

        MENU_BG.update(SCREEN)
        EDIT_MENU.update(SCREEN, time, TIME_DELTA, MOUSE_POS)

        apply_crt_effect(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                screenInput = EDIT_MENU.check_for_input(MOUSE_POS)
                match screenInput:
                    case -1:
                        is_running = False

            if event.type == pygame.KEYDOWN:
                EDIT_MENU.input(event)


        pygame.display.update()

    # pygame.quit()
    # sys.exit()


if __name__ == "__main__":
    mainMenu()
