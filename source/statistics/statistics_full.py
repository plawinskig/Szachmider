import pygame
from source.statistics.player_list import PlayerList
from source.database.datbaseConnector import DatabaseConnector
from source.gui.button import Button

class Statistics():
    def __init__(self, screenWidth, screenHeight):
        self.screenHeight = screenHeight
        self.screenWidth = screenWidth

        DATABASE = DatabaseConnector()

        playerList = DATABASE.get_player_list()
        self.left_side_bar = PlayerList(300, playerList)

        self.BTN_EXIT = Button(pos=(70, 70), text="",
                               imgNormal=pygame.image.load("assets/buttons/BTN_back.png").convert_alpha(),
                               imgHover=pygame.image.load("assets/buttons/BTN_back_hover.png").convert_alpha(),
                               r = 9)



    
    def update(self, screen, time, time_delta, position):
        self.left_side_bar.update(screen, time, time_delta, position)

        for btn in [self.BTN_EXIT]:
            btn.hover(position)
            btn.update(screen, time, time_delta)

    def check_for_input(self, position):
        if self.left_side_bar.check_for_input(position):
            return 1
        if self.BTN_EXIT.check_for_input(position):
            return -1
        return 0
    
    def input(self, event):
        self.left_side_bar.input(event)

    