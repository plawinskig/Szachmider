from peewee import *

db = MySQLDatabase(
    'szachmider',
    user='root',
    password='',
    host='localhost'
)

class Player(Model):
    idP=IntegerField()
    username=CharField(max_length=50,unique=True)

    class Meta:
        database=db