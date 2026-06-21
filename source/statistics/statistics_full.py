import pygame
from pygame import Surface

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

        self.graySurface = pygame.Surface(size=(screenWidth, screenHeight))
        self.graySurface.fill(pygame.Color("#657392"))
        self.whiteSurface = pygame.Surface(size=(screenWidth, screenHeight))
        self.whiteSurface.fill(pygame.Color("#c7cfdd"))

        self.BTN_EXIT = Button(pos=(70, 70), text="",
                               imgNormal=pygame.image.load("assets/buttons/BTN_back.png").convert_alpha(),
                               imgHover=pygame.image.load("assets/buttons/BTN_back_hover.png").convert_alpha(),
                               r = -1)

        self.BTN_WINRATE = Button(pos=(screenWidth/2 + 30, 70), text="Wygrane: 0",
                               imgNormal=pygame.image.load("assets/buttons/BTN_nametag.png").convert_alpha(),
                               imgHover=pygame.image.load("assets/buttons/BTN_nametag.png").convert_alpha(),
                               r = 1)
        
        self.BTN_DRAWRATE = Button(pos=(screenWidth/2 + 30, 140), text="Remisy: 0",
                               imgNormal=pygame.image.load("assets/buttons/BTN_nametag.png").convert_alpha(),
                               imgHover=pygame.image.load("assets/buttons/BTN_nametag.png").convert_alpha(),
                               r = 1)
        
        self.BTN_LOSERATE = Button(pos=(screenWidth/2 + 30, 210), text="Przegrane: 0",
                               imgNormal=pygame.image.load("assets/buttons/BTN_nametag.png").convert_alpha(),
                               imgHover=pygame.image.load("assets/buttons/BTN_nametag.png").convert_alpha(),
                               r = 1)


    
    def update(self, screen: Surface, time, time_delta, position):
        self.left_side_bar.update(screen, time, time_delta, position)

        screen.blit(self.graySurface, (self.screenWidth/3 + 30, 0))
        screen.blit(self.whiteSurface, (self.screenWidth/3 + 36, 0))

        for btn in [self.BTN_EXIT, self.BTN_WINRATE, self.BTN_DRAWRATE, self.BTN_LOSERATE]:
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

    