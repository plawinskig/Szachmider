import pygame
from source.gui.button import Button
from source.menu.play_submenu.player_selection import PlayerSelection
from source.menu.play_submenu.color_selection import ColorButton

class PlayersStartup:
    def __init__(self, position, player_list, screen_width):
        self.x_pos = position[0]
        self.y_pos = position[1]

        self.screen_width = screen_width

        self.player_list = player_list

        self.BTN_BACK = Button(pos=(self.x_pos, 180), text="",
                            img_normal=pygame.image.load("assets/buttons/BTN_back.png").convert_alpha(),
                            img_hover=pygame.image.load("assets/buttons/BTN_back_hover.png").convert_alpha(),
                            r = 9)

        self.fst_player = PlayerSelection(self.x_pos, player_list, r=1, offset=self.screen_width * -0.25)
        self.scnd_player = PlayerSelection(self.x_pos, player_list, r=5, offset=self.screen_width * 0.25 + 40)

        self.BTN_FST_COLOR = ColorButton((self.x_pos - 100, 254), 1, r=3)
        self.BTN_SCND_COLOR = ColorButton((self.x_pos + 100, 254), 2, r=7)

        self.BTN_CHOOSE_BOARD = Button(pos=(self.x_pos, 700), text="Wybierz planszę", 
                                    img_normal=pygame.image.load("assets/buttons/BTN_play.png").convert_alpha(),
                                    img_hover=pygame.image.load("assets/buttons/BTN_play_hover.png").convert_alpha(),
                                    r = -1, text_hover_color=pygame.Color("#5ac54f"))
        self.BTN_CHOOSE_BOARD.alpha = 0
        self.BTN_CHOOSE_BOARD.new_alpha = 0

        self.contains_equal = False

        self.x_dest = self.x_pos
        self.is_moving = False
        self.moving_row = 0
        self.row_delay = 0
        

    def update(self, screen, time, time_delta, mouse_pos):
        if self.is_moving:
            buttons_pos = pygame.math.lerp(self.x_pos, self.x_dest, time_delta * 6, True)
            self.x_pos = buttons_pos
            row = 0
        i = 0

        # Buttons start moving from the side closer to the direction they are moving <- doesn't work sadly
        # Looks more natural that way
        real_buttons_index = [0, 2, 3, 5]
        buttons = [self.BTN_BACK, self.fst_player, self.BTN_FST_COLOR, 
                   self.BTN_SCND_COLOR, self.scnd_player, self.BTN_CHOOSE_BOARD]
        #if (self.x_dest > self.x_pos):
         #   buttons = buttons[::-1]
          #  real_buttons_index = [5, 3, 2, 0]

        for btn in buttons:
            # Logic for moving the buttons
            if self.is_moving:
                if row == self.moving_row and not btn.is_moving:
                    if i == real_buttons_index[0]:
                        btn.move(position=(self.x_dest - self.screen_width * 0.4, btn.y_dest))
                    elif i == real_buttons_index[1]:
                        btn.move(position=(self.x_dest - 100, btn.y_dest))
                    elif i == real_buttons_index[2]:
                        btn.move(position=(self.x_dest + 100, btn.y_dest))
                    elif i == real_buttons_index[3]:
                        btn.move(position=(self.x_dest, btn.y_dest))
                    else:
                        btn.move(self.x_dest)
                if self.row_delay >= 0.3:
                    self.moving_row += 1
                    self.row_delay = 0
                self.row_delay += time_delta
                row += 1
            
            if i in real_buttons_index:
                if (i == real_buttons_index[3] and self.canPlay()):
                    btn.new_alpha = 255
                elif (i == real_buttons_index[3] and not self.canPlay()):
                    btn.new_alpha = 0

                btn.hover(mouse_pos)
                btn.update(screen, time, time_delta)
            else:
                btn.update(screen, time, time_delta, mouse_pos)
            i += 1
        
        if (self.is_moving and not self.fst_player.is_moving
                            and not self.BTN_FST_COLOR.is_moving
                            and not self.BTN_SCND_COLOR.is_moving
                            and not self.scnd_player.is_moving
                            and not self.BTN_BACK.is_moving):
            self.is_moving = False

    def move(self, x_dest):
        self.is_moving = True
        self.x_dest = x_dest + 1
        self.moving_row = 0
    
    def checkForInput(self, position):
        if self.fst_player.checkForInput(position):
            return 1
        elif self.scnd_player.checkForInput(position):
            return 2
        # Changing color of one player also changes the color of the other, 
        # so that they are not the same
        elif self.BTN_FST_COLOR.checkForInput(position):
            if self.BTN_FST_COLOR.color == 1:
                self.BTN_SCND_COLOR.color = 2
            elif self.BTN_FST_COLOR.color == 2:
                self.BTN_SCND_COLOR.color = 1
            else:
                self.BTN_SCND_COLOR.color = 3
            self.BTN_FST_COLOR.updateColor()
            self.BTN_SCND_COLOR.updateColor()
            return 3
        elif self.BTN_SCND_COLOR.checkForInput(position):
            if self.BTN_SCND_COLOR.color == 1:
                self.BTN_FST_COLOR.color = 2
            elif self.BTN_SCND_COLOR.color == 2:
                self.BTN_FST_COLOR.color = 1
            else:
                self.BTN_FST_COLOR.color = 3
            self.BTN_SCND_COLOR.updateColor()
            self.BTN_FST_COLOR.updateColor()
            return 4
        elif self.BTN_BACK.checkForInput(position):
            return 5
        return 0

    def input(self, event):
        self.fst_player.input(event)
        self.scnd_player.input(event)

    def canPlay(self):
        return (self.fst_player.getPlayer() != self.scnd_player.getPlayer()
            and self.fst_player.getPlayer().strip() in self.player_list
            and self.scnd_player.getPlayer().strip() in self.player_list)