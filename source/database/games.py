import os

from peewee import *
from source.database.players import Players
from source.database.boards import Boards

class Games(Model):
    GId=IntegerField(primary_key=True)
    PWhite=ForeignKeyField(Players,column_name="PWhite",null=False)
    PBlack=ForeignKeyField(Players,column_name="PBlack",null=False)
    playedBoard=ForeignKeyField(Boards,column_name="playedBoard",null=False)
    winner=CharField(null=False)
    date=DateField(null=False)

    class Meta:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        DB_PATH = os.path.join(BASE_DIR, 'szachmider.db')
        database=SqliteDatabase(DB_PATH)