import os

from peewee import *

class Players(Model):
    PId=IntegerField(primary_key=True)
    PName=CharField(unique=True,null=False)

    class Meta:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        DB_PATH = os.path.join(BASE_DIR, 'szachmider.db')
        database=SqliteDatabase(DB_PATH)