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

        self.playerList = DATABASE.get_player_list()
        self.left_side_bar = PlayerList(300, self.playerList)

        del DATABASE

        self.graySurface = pygame.Surface(size=(screenWidth, screenHeight))
        self.graySurface.fill(pygame.Color("#657392"))
        self.whiteSurface = pygame.Surface(size=(screenWidth, screenHeight))
        self.whiteSurface.fill(pygame.Color("#c7cfdd"))

        self.BTN_EXIT = Button(pos=(70, 70), text="",
                               imgNormal=pygame.image.load("assets/buttons/BTN_back.png").convert_alpha(),
                               imgHover=pygame.image.load("assets/buttons/BTN_back_hover.png").convert_alpha(),
                               r = -1)

        self.BTN_WINRATE = Button(pos=(6*screenWidth/13, 70), text="Wygrane: 0",
                               imgNormal=pygame.image.load("assets/buttons/BTN_short.png").convert_alpha(),
                               imgHover=pygame.image.load("assets/buttons/BTN_short.png").convert_alpha(),
                               r = 1)
        
        self.BTN_DRAWRATE = Button(pos=(6*screenWidth/13, 130), text="Remisy: 0",
                               imgNormal=pygame.image.load("assets/buttons/BTN_short.png").convert_alpha(),
                               imgHover=pygame.image.load("assets/buttons/BTN_short.png").convert_alpha(),
                               r = 2)
        
        self.BTN_LOSERATE = Button(pos=(6*screenWidth/13, 190), text="Przegrane: 0",
                               imgNormal=pygame.image.load("assets/buttons/BTN_short.png").convert_alpha(),
                               imgHover=pygame.image.load("assets/buttons/BTN_short.png").convert_alpha(),
                               r = 3)
        
        self.BTN_TITLE_LOSER = Button(pos=(screenWidth - 300, 70), text="Ofiara:",
                               imgNormal=pygame.image.load("assets/buttons/BTN_nametag.png").convert_alpha(),
                               imgHover=pygame.image.load("assets/buttons/BTN_nametag.png").convert_alpha(),
                               r = 4)
        
        self.BTN_PLAYER_LOSER = Button(pos=(screenWidth - 300, 130), text="",
                               imgNormal=pygame.image.load("assets/buttons/BTN_nametag.png").convert_alpha(),
                               imgHover=pygame.image.load("assets/buttons/BTN_nametag.png").convert_alpha(),
                               r = 5)
        
        self.BTN_TITLE_ENEMY = Button(pos=(screenWidth - 300, 220), text="Rywal:",
                               imgNormal=pygame.image.load("assets/buttons/BTN_nametag.png").convert_alpha(),
                               imgHover=pygame.image.load("assets/buttons/BTN_nametag.png").convert_alpha(),
                               r = 6)
        
        self.BTN_PLAYER_ENEMY = Button(pos=(screenWidth - 300, 280), text="",
                               imgNormal=pygame.image.load("assets/buttons/BTN_nametag.png").convert_alpha(),
                               imgHover=pygame.image.load("assets/buttons/BTN_nametag.png").convert_alpha(),
                               r = 7)
        
        self.BTN_DELETE = Button(pos=(screenWidth - 300, screenHeight - 50), text="Usuń gracza",
                               imgNormal=pygame.image.load("assets/buttons/BTN_exit.png").convert_alpha(),
                               imgHover=pygame.image.load("assets/buttons/BTN_exit_hover.png").convert_alpha(),
                               r = -2, textHoverColor=pygame.Color("#c42430"))
        
        

        
        


    
    def update(self, screen: Surface, time, time_delta, position):
        if self.left_side_bar.TEXT_FIELD.text.strip() in self.playerList:
            self._show_stats(self.left_side_bar.TEXT_FIELD.text.strip())
        else:
            self._show_stats("")
            
        self.left_side_bar.update(screen, time, time_delta, position)

        screen.blit(self.graySurface, (self.screenWidth/3 + 30, 0))
        screen.blit(self.whiteSurface, (self.screenWidth/3 + 36, 0))

        for btn in [self.BTN_EXIT, self.BTN_WINRATE, self.BTN_DRAWRATE, self.BTN_LOSERATE,
                    self.BTN_TITLE_LOSER, self.BTN_PLAYER_LOSER, self.BTN_TITLE_ENEMY, self.BTN_PLAYER_ENEMY,
                    self.BTN_DELETE]:
            btn.hover(position)
            btn.update(screen, time, time_delta)

    def check_for_input(self, position):
        if self.left_side_bar.check_for_input(position):
            return 1
        if self.BTN_EXIT.check_for_input(position):
            return -1
        if self.BTN_DELETE.check_for_input(position):
            player = self.left_side_bar.TEXT_FIELD.text.strip()
            if player in self.playerList and player not in ["Random Bot", "Greedy Bot"]:
                DATABASE = DatabaseConnector()
                DATABASE.delete_player(DATABASE.get_player_id(player))
                del DATABASE
                self.left_side_bar.TEXT_FIELD.text = ""
                self.playerList.remove(player)
                self.left_side_bar.filtrate_player_list("")
            return 2
        return 0
    
    def input(self, event):
        self.left_side_bar.input(event)

    def _show_stats(self, player: str):
        if player == "":
            wins, loses, draws = 0, 0, 0
            loser, enemy = "- brak -", "- brak -"
        else:
            DATABASE = DatabaseConnector()
            playerId = DATABASE.get_player_id(player)

            wins, loses = DATABASE.get_player_win_lose(playerId)
            draws = DATABASE.get_player_draws(playerId)
            loser = DATABASE.get_player_most_won_against(playerId)
            enemy = DATABASE.get_player_most_lost_against(playerId)

        self.BTN_WINRATE.text = self.BTN_WINRATE.text.split(" ")[0] + " " + str(wins)
        self.BTN_LOSERATE.text = self.BTN_LOSERATE.text.split(" ")[0] + " " + str(loses)
        self.BTN_DRAWRATE.text = self.BTN_DRAWRATE.text.split(" ")[0] + " " + str(draws)
        self.BTN_PLAYER_LOSER.text = loser
        self.BTN_PLAYER_ENEMY.text = enemy



    