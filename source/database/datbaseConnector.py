import datetime
import os
import sqlite3
from collections import Counter

from peewee import *

from source.database.moveHistory import MoveHistory
from source.database.players import Players
from source.database.games import Games
from source.database.boards import Boards

class DatabaseConnector:

    def __init__(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        DB_PATH = os.path.join(BASE_DIR, 'szachmider.db')
        self.__database = SqliteDatabase(DB_PATH)
        self.__database.connect()

    def __del__(self):
        self.__database.close()

    # returns False if player exists
    def add_player(self, playerName: str) -> bool:
        success = True
        try:
            Players.create(PName=playerName)
        except sqlite3.IntegrityError:
            success = False

        return success


    def add_board(self, file: str) -> bool:
        success = True
        try:
            Boards.create(fileName=file)
        except sqlite3.IntegrityError:
            success = False

        return success

    def delete_player(self,playerId: int):
        Games.update(PWhite=0).where(Games.PWhite == playerId).execute()
        Games.update(PBlack=0).where(Games.PBlack == playerId).execute()
        Players.delete().where(Players.PId==playerId).execute()

    def get_player_id(self, player_name: str) -> int:
        return Players.get(Players.PName == player_name).PId

    def get_player_list(self) -> list[str]:
        db_player_list = Players.select(Players.PName).where(Players.PId>0) # jeśli chcemy dać DeletedUser jako blanket na nieistniejących już użytkowników
        return [p.PName for p in db_player_list]

    def add_game(self, whiteID: int, blackID: int, boardID: int, winner: str = 'N', date: str = str(datetime.date.today())):
        Games.create(PWhite=whiteID, PBlack=blackID, playedBoard=boardID, winner=winner, date=date)

    def define_winner(self, gameID:int, winner: str): # winner is a char: W, B, D or N
        Games.update(winner=winner).where(Games.GId==gameID).execute()

    def get_games(self, whiteID: int, blackID: int, boardID: int, winner: str = 'N', date: str = str(datetime.date.today())):
        return [g.GId for g in Games.select(Games.GId).where(Games.PWhite == whiteID, 
                                                             Games.PBlack == blackID,
                                                             Games.playedBoard == boardID,
                                                             Games.winner == winner,
                                                             Games.date == date)]

    def get_games_move_history(self, gameID: int):
        history = MoveHistory.select(MoveHistory.turn,MoveHistory.pieceId,MoveHistory.moveX,MoveHistory.moveY).where(MoveHistory.game==gameID).tuples()
        return [(turn, piece, (x, y)) for turn, piece, x, y in history]

    def find_games_on_board(self, boardID: int) -> list[int]:
        return [g.GId for g in Games.select(Games.GId).where(Games.playedBoard == boardID)]

    def delete_game(self, gameID: int):
        MoveHistory.delete().where(MoveHistory.game == gameID).execute()
        Games.delete().where(Games.GId == gameID).execute()

    # checks for unique filename - returns False if board with given filename already exists
    def add_board(self, file: str) -> bool:
        success = True
        try:
            Boards.create(fileName=file)
        except sqlite3.IntegrityError:
            success = False

        return success

    def get_board_id(self, boardName: str) -> int:
        return Boards.get(Boards.fileName == boardName).BId

    def delete_board(self, boardID: int): # deletes games played on that board
        gamesToDelete=self.find_games_on_board(boardID)
        for g in gamesToDelete:
            self.delete_game(g)

        Boards.delete().where(Boards.BId == boardID).execute()

    def add_move_to_history(self, gameID: int, turn: int, pieceId: str, x: int, y: int):
        MoveHistory.create(game=gameID, turn=turn, pieceID=pieceId, moveX=x, moveY=y)

    def get_player_win_lose(self, playerID: int) -> tuple[int,int]:
        wins = Games.select().where(
            ((Games.PWhite == playerID) & (Games.winner == 'W')) |
            ((Games.PBlack == playerID) & (Games.winner == 'B'))
        ).count()
        loses = Games.select().where(
            ((Games.PWhite == playerID) & (Games.winner == 'B')) |
            ((Games.PBlack == playerID) & (Games.winner == 'W'))
        ).count()

        return wins, loses

    def get_player_draws(self, playerID: int) -> int:
        return Games.select().where(
            ((Games.PWhite == playerID) | (Games.PBlack == playerID))
            & (Games.winner == 'D')
        ).count()

    def get_ranking(self) -> list[tuple[str,int]]: #username,points
        playerIDs=[(p.PId,p.PName) for p in Players.select(Players.PId,Players.PName)]
        ranking = []
        for pID,pName in playerIDs:
            wins, loses = self.get_player_win_lose(pID)
            draws = self.get_player_draws(pID)
            points = wins*2 + draws
            ranking.append((pName,points))

        ranking.sort(key=lambda x: x[1],reverse=True)
        return ranking

    def get_player_most_won_against(self, playerID: int) -> str: #returns username
        defeatedPlayersW: list[int] = [g.PWhite for g in
            Games.select(Games.PWhite).where(
                (Games.PBlack == playerID) & (Games.winner == 'B')
            )
        ]
        defeatedPlayersB: list[int] = [g.PBlack for g in
            Games.select(Games.PBlack).where(
                (Games.PWhite == playerID) & (Games.winner == 'W')
            )
        ]

        defeatedPlayersW.extend(defeatedPlayersB)
        mostDeafeated = Counter(defeatedPlayersW).most_common(1)[0][0]

        return Players.get(Players.PId == mostDeafeated).PName

    def get_player_most_lost_against(self, playerID: int) -> str: #returns username
        winnerPlayersW: list[int] = [g.PWhite for g in
            Games.select(Games.PWhite).where(
                (Games.PBlack == playerID) & (Games.winner == 'W')
            )
        ]
        winnnerPlayersB: list[int] = [g.PBlack for g in
            Games.select(Games.PBlack).where(
                (Games.PWhite == playerID) & (Games.winner == 'B')
            )
        ]

        winnerPlayersW.extend(winnnerPlayersB)
        bestWinner = Counter(winnerPlayersW).most_common(1)[0][0]

        return Players.get(Players.PId == bestWinner).PName