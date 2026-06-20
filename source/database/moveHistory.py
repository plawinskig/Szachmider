import os

from peewee import *
from source.database.games import Games

class MoveHistory(Model):
    game=ForeignKeyField(Games,null=False)
    turn=IntegerField()
    pieceId=CharField(null=False)
    moveX=IntegerField(null=False)
    moveY=IntegerField(null=False)

    class Meta:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        DB_PATH = os.path.join(BASE_DIR, 'szachmider.db')
        database=SqliteDatabase(DB_PATH)
        primary_key = CompositeKey('game', 'turn')