from source.gui.button import Button
import pygame

class MainButtons():
    def __init__(self, x_pos, screen_width):

        self.screen_width = screen_width
        self.x_pos = x_pos

        self.x_dest = self.x_pos
        self.is_moving = False
        self.moving_row = 0
        self.row_delay = 0

        self.BTN_PLAY = Button(pos=(self.x_pos, 254), text="Graj",
                            img_normal=pygame.image.load("assets/buttons/BTN_play.png").convert_alpha(),
                            img_hover=pygame.image.load("assets/buttons/BTN_play_hover.png").convert_alpha(), r=1,
                            text_hover_color=pygame.Color("#5ac54f"))

        self.BTN_STATISTICS = Button(pos=(self.x_pos, 323), text="Statystyki",
                            img_normal=pygame.image.load("assets/buttons/BTN_statistics.png").convert_alpha(),
                            img_hover=pygame.image.load("assets/buttons/BTN_statistics_hover.png").convert_alpha(), r=2,
                            text_hover_color=pygame.Color("#0098dc"))

        self.BTN_EDIT = Button(pos=(self.x_pos, 392), text="Plansze",
                            img_normal=pygame.image.load("assets/buttons/BTN_edit.png").convert_alpha(),
                            img_hover=pygame.image.load("assets/buttons/BTN_edit_hover.png").convert_alpha(), r=3,
                            text_hover_color=pygame.Color("#0098dc"))

        self.BTN_EXIT = Button(pos=(self.x_pos, 461), text="Wyjdź",
                            img_normal=pygame.image.load("assets/buttons/BTN_exit.png").convert_alpha(),
                            img_hover=pygame.image.load("assets/buttons/BTN_exit_hover.png").convert_alpha(), r=4,
                            text_hover_color=pygame.Color("#c42430"))

    def update(self, screen, time, time_delta, position):
        if self.is_moving:
            buttons_pos = pygame.math.lerp(self.x_pos, self.x_dest, time_delta * 6, True)
            self.x_pos = buttons_pos
            row = 0
        for btn in [self.BTN_PLAY, self.BTN_STATISTICS, self.BTN_EDIT, self.BTN_EXIT]:
            # Logic for moving the buttons 
            if self.is_moving:
                if row == self.moving_row and not btn.is_moving:
                    btn.move(position=(self.x_dest, btn.y_pos))
                if self.row_delay >= 0.3:
                    self.moving_row += 1
                    self.row_delay = 0
                self.row_delay += time_delta
                row += 1
            
            btn.hover(position)
            btn.update(screen, time, time_delta)
        if (self.is_moving and not self.BTN_PLAY.is_moving
                            and not self.BTN_STATISTICS.is_moving 
                            and not self.BTN_EDIT.is_moving 
                            and not self.BTN_EXIT.is_moving):
            self.is_moving = False

    def checkForInput(self, position):
        i = 1
        for btn in [self.BTN_PLAY, self.BTN_STATISTICS, self.BTN_EDIT, self.BTN_EXIT]:
            if btn.checkForInput(position):
                return i
            i += 1
        return 0

    def move(self, x_dest):
        self.is_moving = True
        self.x_dest = x_dest + 1
        self.moving_row = 0