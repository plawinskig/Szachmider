import os

from peewee import *
from players import Players
from boards import Boards

class Games(Model):
    GId=IntegerField(primary_key=True)
    PWhite=ForeignKeyField(Players,null=False)
    PBlack=ForeignKeyField(Players,null=False)
    playedBoard=ForeignKeyField(Boards,null=False)
    winner=CharField(null=False)
    date=DateField(null=False)

    class Meta:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        DB_PATH = os.path.join(BASE_DIR, 'szachmider.db')
        database=SqliteDatabase(DB_PATH)