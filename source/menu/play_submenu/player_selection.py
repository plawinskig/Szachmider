from source.database.datbaseConnector import DatabaseConnector
from source.gui.button import Button
from source.gui.text_field import TextField
import pygame

class PlayerSelection():
    def __init__(self, xPos, playerList, r = 0, offset=0):
        self.xPos = xPos
        self.playerList = playerList

        self.xDest = self.xPos
        self.isMoving = False
        self.movingRow = 0
        self.rowDelay = 0

        self.r = r
        self.offset = offset

        self.TEXT_FIELD = TextField(pos=(self.xPos, 254), text="",
                                    img_normal=pygame.image.load("assets/buttons/BTN_text_player.png").convert_alpha(),
                                    imgHover=pygame.image.load("assets/buttons/BTN_text_player_hover.png").convert_alpha(),
                                    r = r + 1)
        
        self.BTN_UP = Button(pos=(self.xPos - 21, 324), text="",
                             imgNormal=pygame.image.load("assets/buttons/BTN_arrow_up.png").convert_alpha(),
                             imgHover=pygame.image.load("assets/buttons/BTN_arrow_up_hover.png").convert_alpha(),
                             r = r + 2)
        
        # Dummy button for better looking movement of BTN_DOWN, 
        # so it's not moved with the same speed as the player list
        self.BTN_EMPTY = Button(pos=(self.xPos - 21, 464), text="",
                                imgNormal=pygame.image.load("assets/buttons/BTN_nametag.png").convert_alpha(),
                                imgHover=pygame.image.load("assets/buttons/BTN_nametag_hover.png").convert_alpha(),
                                r = 0)
        self.BTN_EMPTY.alpha = 0
        self.BTN_EMPTY.newAlpha = 0
        
        self.BTN_DOWN = Button(pos=(self.xPos - 21, 604), text="",
                               imgNormal=pygame.image.load("assets/buttons/BTN_arrow_down.png").convert_alpha(),
                               imgHover=pygame.image.load("assets/buttons/BTN_arrow_down_hover.png").convert_alpha(),
                               r = r + 3)
        
        self.BTN_PLAYER_LIST = []
        self.tempPlayerList = []

        self.containsEqual = True
        self.set_player_list(self.playerList)
        
    def update(self, screen, time, time_delta, position):
        if self.isMoving:
            buttons_pos = pygame.math.lerp(self.xPos, self.xDest, time_delta * 6, True)
            self.xPos = buttons_pos
            row = 0
        for btn in [self.TEXT_FIELD, self.BTN_UP, self.BTN_EMPTY, self.BTN_DOWN]:
            # Logic for moving the buttons
            if self.isMoving:
                if row == self.movingRow and not btn.isMoving:
                    if row >= 1:
                        btn.move(position=(self.xDest - 21, btn.yPos))
                    else:
                        btn.move(position=(self.xDest, btn.yPos))
                if self.rowDelay >= 0.3:
                    self.movingRow += 1
                    self.rowDelay = 0
                self.rowDelay += time_delta
                row += 1
            
            btn.hover(position)
            btn.update(screen, time, time_delta)
        
        # Logic for moving the player list
        for btn in self.BTN_PLAYER_LIST:
            if self.isMoving and not btn.isMoving and self.movingRow > 1:
                btn.move(position=(self.xDest - 21, btn.yDest))
            
            btn.hover(position)
            btn.update(screen, time, time_delta)

        if (self.isMoving and not self.TEXT_FIELD.isMoving
                            and not self.BTN_UP.isMoving
                            and not self.BTN_EMPTY.isMoving
                            and not self.BTN_DOWN.isMoving):
            self.isMoving = False
        
    def check_for_input(self, position):
        i = 1
        for btn in [self.TEXT_FIELD, self.BTN_UP, self.BTN_DOWN]:
            if btn.check_for_input(position):
                if i == 2:
                    self.move_the_list(-1)
                elif i == 3:
                    self.move_the_list(1)
                return i
            i += 1
        
        for btn in self.BTN_PLAYER_LIST:
            if btn.check_for_input(position):
                if not self.containsEqual and i-3 == len(self.BTN_PLAYER_LIST):
                    # TODO: normalne dodawanie gracza, a nie tylko do listy
                    self.playerList.append(self.TEXT_FIELD.text.strip())
                    dbConnecor=DatabaseConnector()
                    dbConnecor.add_player(self.TEXT_FIELD.text.strip())
                    del dbConnecor
                    self.containsEqual = True
                else:
                    self.TEXT_FIELD.text = btn.text
                    self.TEXT_FIELD.updateText()
                self.filtrate_player_list(self.TEXT_FIELD.text)
                return i
            i += 1
        return 0
    
    def input(self, event):
        self.TEXT_FIELD.input(event)
        self.filtrate_player_list(self.TEXT_FIELD.text)

    def move(self, x_dest):
        self.isMoving = True
        self.xDest = x_dest + 1 + self.offset
        self.movingRow = 0

    def move_the_list(self, direction):
        if ((direction + self.currentListPos) >= 0
            and (direction + self.currentListPos) < self.maxListPos):
            #and not self.BTN_PLAYER_LIST[self.current_list_pos].is_moving):
            self.currentListPos = direction + self.currentListPos
            i = 0
            for btn in self.BTN_PLAYER_LIST:
                btn.move(position=(btn.xDest, btn.yDest + 70 * (-1 * direction)))
                if i <= self.currentListPos - 2 or i >= self.currentListPos + 2:
                    btn.newAlpha = 0
                    if direction == 0:
                        btn.alpha = 0
                elif i == self.currentListPos - 1 or i >= self.currentListPos + 1:
                    btn.newAlpha = 127
                    if direction == 0:
                        btn.alpha = 127
                elif i == self.currentListPos:
                    btn.newAlpha = 255
                    if direction == 0:
                        btn.alpha = 255
                i += 1

    def set_player_list(self, playerList):
        self.tempPlayerList = playerList
        self.BTN_PLAYER_LIST = []
        i = 0
        for player in self.tempPlayerList:
            self.BTN_PLAYER_LIST.append(Button(pos=(self.xPos - 21, 460 + len(self.BTN_PLAYER_LIST) * 70), text=player,
                                               imgNormal=pygame.image.load("assets/buttons/BTN_nametag.png").convert_alpha(),
                                               imgHover=pygame.image.load("assets/buttons/BTN_nametag_hover.png").convert_alpha(),
                                               r = 4 + i))
            i += 1

        if not self.containsEqual:
            i += 1
            self.BTN_PLAYER_LIST.append(Button(pos=(self.xPos - 21, 460 + len(self.BTN_PLAYER_LIST) * 70),
                                               text=self.TEXT_FIELD.text.strip(),
                                               imgNormal=pygame.image.load("assets/buttons/BTN_new_nametag.png").convert_alpha(),
                                               imgHover=pygame.image.load("assets/buttons/BTN_new_nametag_hover.png").convert_alpha(),
                                               r = 4 + i))
        
        self.currentListPos = 0
        self.maxListPos = i
        self.move_the_list(0)

    def filtrate_player_list(self, text):
        if text.strip() == "":
            self.containsEqual = True
            self.set_player_list(self.playerList)
            return
        filteredPlayers = []
        isEqual = False
        for player in self.playerList:
            if text.strip().lower() in player.lower():
                filteredPlayers.append(player)
            if text.strip().lower() == player.lower():
                isEqual = True
        self.containsEqual = isEqual
        self.set_player_list(filteredPlayers)

    def addToList(self, player):
        self.playerList.append(player)
        self.filtrate_player_list(self.TEXT_FIELD.text)

    def getPlayer(self) -> str:
        return self.TEXT_FIELD.text
