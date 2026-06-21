from source.database.datbaseConnector import DatabaseConnector
from source.gui.button import Button
from source.gui.text_field import TextField
import pygame

class PlayerList():
    def __init__(self, xPos, playerList, r = 0, offset=0):
        self.xPos = xPos
        self.playerList = playerList

        self.r = r
        self.offset = offset

        self.TEXT_FIELD = TextField(pos=(self.xPos, 150), text="",
                                    img_normal=pygame.image.load("assets/buttons/BTN_text_player.png").convert_alpha(),
                                    imgHover=pygame.image.load("assets/buttons/BTN_text_player_hover.png").convert_alpha(),
                                    r = r + 1)
        
        self.BTN_UP = Button(pos=(self.xPos - 21, 220), text="",
                             imgNormal=pygame.image.load("assets/buttons/BTN_arrow_up.png").convert_alpha(),
                             imgHover=pygame.image.load("assets/buttons/BTN_arrow_up_hover.png").convert_alpha(),
                             r = r + 2)
        
        self.BTN_DOWN = Button(pos=(self.xPos - 21, 640), text="",
                               imgNormal=pygame.image.load("assets/buttons/BTN_arrow_down.png").convert_alpha(),
                               imgHover=pygame.image.load("assets/buttons/BTN_arrow_down_hover.png").convert_alpha(),
                               r = r + 3)
        
        self.BTN_PLAYER_LIST = []
        self.tempPlayerList = []

        self.set_player_list(self.playerList)
        
    def update(self, screen, time, time_delta, position):
        for btn in [self.TEXT_FIELD, self.BTN_UP, self.BTN_DOWN]:
            btn.hover(position)
            btn.update(screen, time, time_delta)
        
        for btn in self.BTN_PLAYER_LIST:
            btn.hover(position)
            btn.update(screen, time, time_delta)
        
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
                self.TEXT_FIELD.text = btn.text
                self.TEXT_FIELD.updateText()
                self.filtrate_player_list(self.TEXT_FIELD.text)
                return i
            i += 1
        return 0
    
    def input(self, event):
        self.TEXT_FIELD.input(event)
        self.filtrate_player_list(self.TEXT_FIELD.text)

    def move_the_list(self, direction):
        if ((direction + self.currentListPos) >= 0
            and (direction + self.currentListPos) < self.maxListPos):
            #and not self.BTN_PLAYER_LIST[self.current_list_pos].is_moving):
            self.currentListPos = direction + self.currentListPos
            i = 0
            for btn in self.BTN_PLAYER_LIST:
                btn.move(position=(btn.xDest, btn.yDest + 70 * (-1 * direction)))
                if i < self.currentListPos or i > self.currentListPos + 4:
                    btn.newAlpha = 0
                    if direction == 0:
                        btn.alpha = 0
                else:
                    btn.newAlpha = 255
                    if direction == 0:
                        btn.alpha = 255
                i += 1

    def set_player_list(self, playerList):
        self.tempPlayerList = playerList
        self.BTN_PLAYER_LIST = []
        i = 0
        for player in self.tempPlayerList:
            self.BTN_PLAYER_LIST.append(Button(pos=(self.xPos - 21, 290 + len(self.BTN_PLAYER_LIST) * 70), text=player,
                                               imgNormal=pygame.image.load("assets/buttons/BTN_nametag.png").convert_alpha(),
                                               imgHover=pygame.image.load("assets/buttons/BTN_nametag_hover.png").convert_alpha(),
                                               r = 4 + i))
            i += 1
        
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

    def getPlayer(self) -> str:
        return self.TEXT_FIELD.text
