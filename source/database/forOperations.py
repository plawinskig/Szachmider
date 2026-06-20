import sqlite3


if __name__ == "__main__":
    db = sqlite3.connect("szachmider.db")
    curs = db.cursor()

    curs.execute("DROP TABLE MoveHistory")
    curs.execute("DROP TABLE Games")

    db.commit()
    db.close()