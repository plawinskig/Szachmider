
import pygame
from source.menu.choose_board_submenu.choose_boards import ChooseBoard
from source.gui.button import Button

class ChoosingBoardToPlay():
    def __init__(self, position, screen_width, screen_height):
        self.x_pos = position[0]
        self.y_pos = position[1]

        self.screen_width = screen_width

        self.x_dest = self.x_pos
        self.is_moving = False
        self.moving_row = 0
        self.row_delay = 0

        self.BTN_BACK = Button(pos=(self.x_pos, 180), text="",
                            img_normal=pygame.image.load("assets/buttons/BTN_back.png").convert_alpha(),
                            img_hover=pygame.image.load("assets/buttons/BTN_back_hover.png").convert_alpha(),
                            r = 9)
        
        self.board_menu = ChooseBoard(position, screen_width, screen_height)

    def update(self, screen, time, time_delta, mouse_pos):
        if self.is_moving:
            buttons_pos = pygame.math.lerp(self.x_pos, self.x_dest, time_delta * 6, True)
            self.x_pos = buttons_pos
            row = 0
        i = 0

        for btn in [self.BTN_BACK, self.board_menu]:
            if self.is_moving:
                if row == self.moving_row and not btn.is_moving:
                    if i == 0:
                        btn.move(position=(self.x_dest - self.screen_width * 0.4, btn.y_dest))
                    else:
                        btn.move(self.x_dest)
                if self.row_delay >= 0.3:
                    self.moving_row += 1
                    self.row_delay = 0
                self.row_delay += time_delta
                row += 1
            
            if i == 0:
                btn.hover(mouse_pos)
                btn.update(screen, time, time_delta)
            else:
                btn.update(screen, time, time_delta, mouse_pos)
            i += 1
        
        if (self.is_moving and not self.BTN_BACK.is_moving
                            and not self.board_menu.is_moving):
            self.is_moving = False

    def checkForInput(self, position):
        if self.BTN_BACK.checkForInput(position):
            return 1
        else:
            is_board_clicked = self.board_menu.checkForInput(position)
            if is_board_clicked:
                return self.board_menu.getRespectiveBoard(is_board_clicked)
        
        return 0

    def move(self, x_dest):
        self.is_moving = True
        self.x_dest = x_dest + 1
        self.moving_row = 0

