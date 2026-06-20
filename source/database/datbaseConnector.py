import sqlite3


class DatabaseConnector:

    def __init__(self):
        self.__database = sqlite3.connect("szachmider.db")
        self.__cursor = self.__database.cursor()


    def __del__(self):
        self.__database.close()


    def add_player(self, playerName: str):
        self.__cursor.execute(f"INSERT INTO Players(PId, PName) VALUES (NULL, '{playerName}')")
        self.__database.commit()

