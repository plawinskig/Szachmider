from source.database.datbaseConnector import DatabaseConnector
from source.gui.button import Button
from source.gui.text_field import TextField
import pygame

class PlayerSelection():
    def __init__(self, x_pos, player_list, r = 0, offset=0):
        self.x_pos = x_pos
        self.player_list = player_list

        self.x_dest = self.x_pos
        self.is_moving = False
        self.moving_row = 0
        self.row_delay = 0

        self.r = r
        self.offset = offset

        self.TEXT_FIELD = TextField(pos=(self.x_pos, 254), text="",
                                    img_normal=pygame.image.load("assets/buttons/BTN_text_player.png").convert_alpha(),
                                    imgHover=pygame.image.load("assets/buttons/BTN_text_player_hover.png").convert_alpha(),
                                    r = r + 1)
        
        self.BTN_UP = Button(pos=(self.x_pos - 21, 324), text="",
                             imgNormal=pygame.image.load("assets/buttons/BTN_arrow_up.png").convert_alpha(),
                             imgHover=pygame.image.load("assets/buttons/BTN_arrow_up_hover.png").convert_alpha(),
                             r = r + 2)
        
        # Dummy button for better looking movement of BTN_DOWN, 
        # so it's not moved with the same speed as the player list
        self.BTN_EMPTY = Button(pos=(self.x_pos - 21, 464), text="",
                                imgNormal=pygame.image.load("assets/buttons/BTN_nametag.png").convert_alpha(),
                                imgHover=pygame.image.load("assets/buttons/BTN_nametag_hover.png").convert_alpha(),
                                r = 0)
        self.BTN_EMPTY.alpha = 0
        self.BTN_EMPTY.newAlpha = 0
        
        self.BTN_DOWN = Button(pos=(self.x_pos - 21, 604), text="",
                               imgNormal=pygame.image.load("assets/buttons/BTN_arrow_down.png").convert_alpha(),
                               imgHover=pygame.image.load("assets/buttons/BTN_arrow_down_hover.png").convert_alpha(),
                               r = r + 3)
        
        self.BTN_PLAYER_LIST = []
        self.temp_player_list = []

        self.contains_equal = True
        self.setPlayerList(self.player_list)
        
    def update(self, screen, time, time_delta, position):
        if self.is_moving:
            buttons_pos = pygame.math.lerp(self.x_pos, self.x_dest, time_delta * 6, True)
            self.x_pos = buttons_pos
            row = 0
        for btn in [self.TEXT_FIELD, self.BTN_UP, self.BTN_EMPTY, self.BTN_DOWN]:
            # Logic for moving the buttons
            if self.is_moving:
                if row == self.moving_row and not btn.isMoving:
                    if row >= 1:
                        btn.move(position=(self.x_dest - 21, btn.yPos))
                    else:
                        btn.move(position=(self.x_dest, btn.yPos))
                if self.row_delay >= 0.3:
                    self.moving_row += 1
                    self.row_delay = 0
                self.row_delay += time_delta
                row += 1
            
            btn.hover(position)
            btn.update(screen, time, time_delta)
        
        # Logic for moving the player list
        for btn in self.BTN_PLAYER_LIST:
            if self.is_moving and not btn.isMoving and self.moving_row > 1:
                btn.move(position=(self.x_dest - 21, btn.yDest))
            
            btn.hover(position)
            btn.update(screen, time, time_delta)

        if (self.is_moving and not self.TEXT_FIELD.isMoving
                            and not self.BTN_UP.isMoving
                            and not self.BTN_EMPTY.isMoving
                            and not self.BTN_DOWN.isMoving):
            self.is_moving = False
        
    def checkForInput(self, position):
        i = 1
        for btn in [self.TEXT_FIELD, self.BTN_UP, self.BTN_DOWN]:
            if btn.check_for_input(position):
                if i == 2:
                    self.moveTheList(-1)
                elif i == 3:
                    self.moveTheList(1)
                return i
            i += 1
        
        for btn in self.BTN_PLAYER_LIST:
            if btn.check_for_input(position):
                if not self.contains_equal and i-3 == len(self.BTN_PLAYER_LIST):
                    # TODO: normalne dodawanie gracza, a nie tylko do listy
                    self.player_list.append(self.TEXT_FIELD.text.strip())
                    dbConnecor=DatabaseConnector()
                    dbConnecor.add_player(self.TEXT_FIELD.text.strip())
                    del dbConnecor
                    self.contains_equal = True
                else:
                    self.TEXT_FIELD.text = btn.text
                    self.TEXT_FIELD.updateText()
                self.filtratePlayerList(self.TEXT_FIELD.text)
                return i
            i += 1
        return 0
    
    def input(self, event):
        self.TEXT_FIELD.input(event)
        self.filtratePlayerList(self.TEXT_FIELD.text)

    def move(self, x_dest):
        self.is_moving = True
        self.x_dest = x_dest + 1 + self.offset
        self.moving_row = 0

    def moveTheList(self, direction):
        if ((direction + self.current_list_pos) >= 0 
            and (direction + self.current_list_pos) < self.max_list_pos):
            #and not self.BTN_PLAYER_LIST[self.current_list_pos].is_moving):
            self.current_list_pos = direction + self.current_list_pos
            i = 0
            for btn in self.BTN_PLAYER_LIST:
                btn.move(position=(btn.xDest, btn.yDest + 70 * (-1 * direction)))
                if i <= self.current_list_pos - 2 or i >= self.current_list_pos + 2:
                    btn.newAlpha = 0
                    if direction == 0:
                        btn.alpha = 0
                elif i == self.current_list_pos - 1 or i >= self.current_list_pos + 1:
                    btn.newAlpha = 127
                    if direction == 0:
                        btn.alpha = 127
                elif i == self.current_list_pos:
                    btn.newAlpha = 255
                    if direction == 0:
                        btn.alpha = 255
                i += 1

    def setPlayerList(self, player_list):
        self.temp_player_list = player_list
        self.BTN_PLAYER_LIST = []
        i = 0
        for player in self.temp_player_list:
            self.BTN_PLAYER_LIST.append(Button(pos=(self.x_pos - 21, 460 + len(self.BTN_PLAYER_LIST) * 70), text=player,
                                               imgNormal=pygame.image.load("assets/buttons/BTN_nametag.png").convert_alpha(),
                                               imgHover=pygame.image.load("assets/buttons/BTN_nametag_hover.png").convert_alpha(),
                                               r = 4 + i))
            i += 1

        if not self.contains_equal:
            i += 1
            self.BTN_PLAYER_LIST.append(Button(pos=(self.x_pos - 21, 460 + len(self.BTN_PLAYER_LIST) * 70),
                                               text=self.TEXT_FIELD.text.strip(),
                                               imgNormal=pygame.image.load("assets/buttons/BTN_new_nametag.png").convert_alpha(),
                                               imgHover=pygame.image.load("assets/buttons/BTN_new_nametag_hover.png").convert_alpha(),
                                               r = 4 + i))
        
        self.current_list_pos = 0
        self.max_list_pos = i
        self.moveTheList(0)

    def filtratePlayerList(self, text):
        if text.strip() == "":
            self.contains_equal = True
            self.setPlayerList(self.player_list)
            return
        filtred_players = []
        is_equal = False
        for player in self.player_list:
            if text.strip().lower() in player.lower():
                filtred_players.append(player)
            if text.strip().lower() == player.lower():
                is_equal = True
        self.contains_equal = is_equal
        self.setPlayerList(filtred_players)

    def addToList(self, player):
        self.player_list.append(player)
        self.filtratePlayerList(self.TEXT_FIELD.text)

    def getPlayer(self) -> str:
        return self.TEXT_FIELD.text
