import sqlite3


class DatabaseConnector:

    def __init__(self):
        self.__database = sqlite3.connect("szachmider.db")
        self.__cursor = self.__database.cursor()


    def __del__(self):
        self.__database.close()

    # returns False if player exists
    def add_player(self, playerName: str) -> bool:
        success = True
        try:
            self.__cursor.execute(f"INSERT INTO Players(PId, PName) VALUES (NULL, '{playerName}')")
            self.__database.commit()
        except sqlite3.IntegrityError:
            success = False

        return success



    def get_games_move_history(self, gameID: int):
        return [(turn, piece, location) for turn, piece, *location in self.__cursor.execute(f"SELECT turn, pieceID, moveX, moveY  FROM MoveHistory WHERE game == {gameID}")]