import sqlite3

db = sqlite3.connect("szachmider.db")

commands = open("dbSetup.txt", "r")


cursor = db.cursor()

for c in commands:
    try:
        cursor.execute(c.strip())
    except:
        pass
db.commit()
db.close()
commands.close()