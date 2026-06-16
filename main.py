import pygame
import sys

from source.menu.play_submenu.player_selection import PlayerSelection
from source.menu.logo import Logo
from source.menu.menu_background import MenuBackground
from source.menu.main_buttons import MainButtons
from source.menu.play_submenu.players_startup import PlayersStartup

from source.board.board import Board
from source.board.board_view import BoardView
from source.board.square import *

from source.board.move import Move
from source.board.piece import Rook, Knight, Bishop, Queen, King, Pawn
from source.gui.button import Button

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

    render_game = False
    selected_square = None
    is_white_turn = True

    BTN_START_GAME = Button(pos=(play_destination_offscreen, SCREEN_HEIGHT - 120), text="Rozpocznij Grę",
                            img_normal=pygame.image.load("assets/buttons/BTN_play.png").convert_alpha(),
                            img_hover=pygame.image.load("assets/buttons/BTN_play_hover.png").convert_alpha(), r=10)

    # TEST ONLY - Brudnopis że tak to nazwe
    board = Board(8, 8)
    board.set_square(0, 0, BasicSquare())
    board.set_square(1, 0, TeleportSquare()) 
    board.set_square(2, 0, TrapSquare())
    board.set_square(3, 0, HeartSquare())
    board.set_square(4, 0, ShieldSquare())
    board.set_square(5, 0, GrassSquare())

    for x in range(8):
        board.set_piece(x, 1, Pawn(True))
        board.set_piece(x, 6, Pawn(False))
    
    board.set_piece(0, 0, Rook(True)); board.set_piece(7, 0, Rook(True))
    board.set_piece(1, 0, Knight(True)); board.set_piece(6, 0, Knight(True))
    board.set_piece(2, 0, Bishop(True)); board.set_piece(5, 0, Bishop(True))
    board.set_piece(3, 0, Queen(True)); board.set_piece(4, 0, King(True))
    
    board.set_piece(0, 7, Rook(False)); board.set_piece(7, 7, Rook(False))
    board.set_piece(1, 7, Knight(False)); board.set_piece(6, 7, Knight(False))
    board.set_piece(2, 7, Bishop(False)); board.set_piece(5, 7, Bishop(False))
    board.set_piece(3, 7, Queen(False)); board.set_piece(4, 7, King(False))
    
    board.make_movement_matrix()

    boardView = BoardView(board, SCREEN_WIDTH, SCREEN_HEIGHT)

    while is_running:
        SCREEN.blit(BG, (0, 0))

        MOUSE_POS = pygame.mouse.get_pos()
        TIME_DELTA = CLOCK.tick(60) / 1000.0
        time = time + TIME_DELTA

        if time < 0:
            time = 0

        if not render_game:
            MENU_BG.update(SCREEN)
            LOGO.update(SCREEN, time, MOUSE_POS)

        if render_play_menu or PLAY_MENU.is_moving:
            PLAY_MENU.update(SCREEN, time, TIME_DELTA, MOUSE_POS)
            
            if PLAY_MENU.is_moving:
                BTN_START_GAME.move((PLAY_MENU.x_pos, BTN_START_GAME.y_dest))
            BTN_START_GAME.hover(MOUSE_POS)
            BTN_START_GAME.update(SCREEN, time, TIME_DELTA)

        if render_main_menu or MAIN_BTNS.is_moving:
            MAIN_BTNS.update(SCREEN, time, TIME_DELTA, MOUSE_POS)

        if render_game:
            boardView.display(SCREEN, False)

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
                            BTN_START_GAME.move((play_pos, BTN_START_GAME.y_pos))
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
                            BTN_START_GAME.move((play_destination_offscreen, BTN_START_GAME.y_pos))
                            render_play_menu = False
                            render_main_menu = True
                            MAIN_BTNS.move(buttons_pos)
                    
                    if BTN_START_GAME.checkForInput(MOUSE_POS) and not PLAY_MENU.is_moving:
                        render_play_menu = False
                        render_game = True

                if render_game and event.button == 1:
                    mouse_x, mouse_y = MOUSE_POS
                    bx = int((mouse_x - boardView.x_offset) // boardView.x_tile_size)
                    by = int((mouse_y - boardView.y_offset) // boardView.y_tile_size)
                    
                    if 0 <= bx < board.width and 0 <= by < board.height:
                        clicked_pos = (bx, by)
                        clicked_piece = board.get_piece(bx, by)
                        
                        if selected_square is None:
                            if clicked_piece is not None:
                                if clicked_piece.is_black() != is_white_turn:
                                    selected_square = clicked_pos
                                    print(f"Zaznaczono: {clicked_piece.get_code()} na {clicked_pos}")
                        
                        else:
                            from_x, from_y = selected_square
                            attempted_move = Move(from_x, from_y, bx, by)
                            
                            if board.is_valid_move(attempted_move):
                                board.move_piece(attempted_move)
                                board.make_movement_matrix()
                                
                                is_white_turn = not is_white_turn
                                print(f"Wykonano ruch na {clicked_pos}!")
                            else:
                                print("Anulowano zaznaczenie lub nielegalny ruch.")
                            
                            selected_square = None

            if event.type == pygame.KEYDOWN:
                PLAY_MENU.input(event)
            
        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    mainMenu()