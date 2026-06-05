from source.gui.button import Button
from source.gui.text_field import TextField
import pygame

class PlayerSelection():
    def __init__(self, x_pos, player_list):
        self.x_pos = x_pos
        self.player_list = player_list

        self.x_dest = self.x_pos
        self.is_moving = False
        self.moving_row = 0
        self.row_delay = 0

        self.TEXT_FIELD = TextField(pos=(self.x_pos, 250), text="", 
                           img_normal=pygame.image.load("assets/buttons/BTN_text_player.png").convert_alpha(),
                           img_hover=pygame.image.load("assets/buttons/BTN_text_player_hover.png").convert_alpha(),
                           r = 1)
        
        self.BTN_UP = Button(pos=(self.x_pos - 21, 320), text="",
                            img_normal=pygame.image.load("assets/buttons/BTN_arrow_up.png").convert_alpha(),
                            img_hover=pygame.image.load("assets/buttons/BTN_arrow_up_hover.png").convert_alpha(),
                            r = 2)
        
        self.BTN_DOWN = Button(pos=(self.x_pos - 21, 600), text="",
                            img_normal=pygame.image.load("assets/buttons/BTN_arrow_down.png").convert_alpha(),
                            img_hover=pygame.image.load("assets/buttons/BTN_arrow_down_hover.png").convert_alpha(),
                            r = 3)
        
        self.BTN_PLAYER_LIST = []
        i = 0
        for player in self.player_list:
            self.BTN_PLAYER_LIST.append(Button(pos=(self.x_pos - 21, 390 + len(self.BTN_PLAYER_LIST) * 70), text=player,
                            img_normal=pygame.image.load("assets/buttons/BTN_nametag.png").convert_alpha(),
                            img_hover=pygame.image.load("assets/buttons/BTN_nametag.png").convert_alpha(),
                            r = 4 + i))
            i += 1
        
        self.current_list_pos = 1
        self.max_list_pos = i

        self.moveTheList(-1)
        
    def update(self, screen, time, time_delta, position):
        if self.is_moving:
            buttons_pos = pygame.math.lerp(self.x_pos, self.x_dest, time_delta * 6, True)
            self.x_pos = buttons_pos
            row = 0
        for btn in [self.TEXT_FIELD, self.BTN_UP, self.BTN_DOWN]:
            # Logic for moving the buttons
            if self.is_moving:
                if row == self.moving_row and not btn.is_moving:
                    if row >= 1:
                        btn.move(position=(self.x_dest - 21, btn.y_pos))
                    else:
                        btn.move(position=(self.x_dest, btn.y_pos))
                if self.row_delay >= 0.3:
                    self.moving_row += 1
                    self.row_delay = 0
                self.row_delay += time_delta
                row += 1
            
            btn.hover(position)
            btn.update(screen, time, time_delta)
        
        # Logic for moving the player list
        for btn in self.BTN_PLAYER_LIST:
            if self.is_moving and self.moving_row > 1:
                btn.move(position=(self.x_dest - 21, btn.y_pos))
            
            btn.hover(position)
            btn.update(screen, time, time_delta)

        if (self.is_moving and not self.TEXT_FIELD.is_moving
                            and not self.BTN_UP.is_moving 
                            and not self.BTN_DOWN.is_moving):
            self.is_moving = False
        
    def checkForInput(self, position):
        i = 1
        for btn in [self.TEXT_FIELD, self.BTN_UP, self.BTN_DOWN]:
            if btn.checkForInput(position):
                if i == 2:
                    self.moveTheList(-1)
                elif i == 3:
                    self.moveTheList(1)
                return i
            i += 1
        
        for btn in self.BTN_PLAYER_LIST:
            if btn.checkForInput(position):
                if i - 4 < self.current_list_pos:
                    self.moveTheList(-1)
                elif i - 4 > self.current_list_pos:
                    self.moveTheList(1)
                self.TEXT_FIELD.text = btn.text
                self.TEXT_FIELD.updateText()
                return i
            i += 1
        return 0
    
    def input(self, event):
        self.TEXT_FIELD.input(event)

    def move(self, x_dest):
        self.is_moving = True
        self.x_dest = x_dest + 1
        self.moving_row = 0

    def moveTheList(self, direction):
        if ((direction + self.current_list_pos) >= 0 
            and (direction + self.current_list_pos) < self.max_list_pos
            and not self.BTN_PLAYER_LIST[self.current_list_pos].is_moving):
            self.current_list_pos = direction + self.current_list_pos
            i = 0
            for btn in self.BTN_PLAYER_LIST:
                btn.move(position=(btn.x_pos, btn.y_pos + 70 * (-1 * direction)))
                if i <= self.current_list_pos - 2 or i >= self.current_list_pos + 2:
                    btn.new_alpha = 0
                elif i == self.current_list_pos - 1 or i >= self.current_list_pos + 1:
                    btn.new_alpha = 127
                elif i == self.current_list_pos:
                    btn.new_alpha = 255
                i += 1
