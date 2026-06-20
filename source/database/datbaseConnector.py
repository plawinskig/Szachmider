import os
import sqlite3
from collections import Counter

from peewee import *

from Szachmider.source.database.moveHistory import MoveHistory
from Szachmider.source.database.players import Players
from Szachmider.source.database.games import Games

class DatabaseConnector:

    def __init__(self):
        # self.__database = sqlite3.connect("szachmider.db")
        # self.__cursor = self.__database.cursor()
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
            # self.__cursor.execute(f"INSERT INTO Players(PId, PName) VALUES (NULL, '{playerName}')")
            # self.__database.commit()
            Players.create(PName=playerName)
        except sqlite3.IntegrityError:
            success = False

        return success

    def delete_player(self,playerId: int):
        qry=Players.delete().where(Players.PId==playerId)
        qry.execute()

    def get_player_list(self) -> list[str]:
        db_player_list = Players.select(Players.PName).where(Players.PId>0) # jeśli chcemy dać DeletedUser jako blanket na nieistniejących już użytkowników
        return [p.PName for p in db_player_list]

    def get_games_move_history(self, gameID: int):
        #return [(turn, piece, location) for turn, piece, *location in self.__cursor.execute(f"SELECT turn, pieceID, moveX, moveY  FROM MoveHistory WHERE game == {gameID}")]
        history = MoveHistory.select(MoveHistory.turn,MoveHistory.pieceId,MoveHistory.moveX,MoveHistory.moveY).where(MoveHistory.game==gameID).tuples()
        return [(turn, piece, (x, y)) for turn, piece, x, y in history]

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