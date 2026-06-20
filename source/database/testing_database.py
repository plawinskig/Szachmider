from datbaseConnector import DatabaseConnector

db=DatabaseConnector()
list=db.get_player_list()
print(list)

del db