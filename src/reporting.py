import sqlite3
import sqlite3 as sql

from src.database import Database

db = Database()


def report_table():
    try:
        db.cursor.execute(
            """CREATE TABLE IF NOT EXISTS reports
            (OwnerID INTEGER NULL UNIQUE,
            login_count INTEGER NULL, 
            link_opens INTEGER NULL)
            ;"""
        )
        db.connection.commit()
    except sql.OperationalError:
        pass


def view_report_table():
    db.cursor.execute("SELECT rowid, * FROM reports")
    print(db.cursor.fetchall())


def count_user_bookmarks(active_id):
    db.cursor.execute("SELECT rowid FROM bookmarks WHERE OwnerID=(?)", (active_id,))
    count = len([x[0] for x in db.cursor.fetchall()])
    return count


def access_logging(active_id, count):
    num = ([x[0] for x in db.cursor.execute("SELECT link_opens FROM reports WHERE OwnerID=(?)", (active_id,))])
    new_count = num[0] + count
    print(new_count)
    db.cursor.execute("UPDATE reports SET link_opens=(?) WHERE OwnerID=(?)", (new_count, active_id))
    db.connection.commit()


def show_access(active_id):
    num = ([x[0] for x in db.cursor.execute("SELECT link_opens FROM reports WHERE OwnerID=(?)", (active_id,))])
    return num[0]


def login_logging(active_id, count):
    try:
        db.cursor.execute("INSERT INTO reports (OwnerID, login_count, link_opens) VALUES (?,?,?)",
                          (active_id, count, 0))
        db.connection.commit()
        print("first login on this account")
    except sqlite3.IntegrityError as e:
        num = ([x[0] for x in db.cursor.execute("SELECT login_count FROM reports WHERE OwnerID=(?)", (active_id,))])
        new_count = num[0] + count
        print(new_count)
        db.cursor.execute("UPDATE reports SET login_count=(?) WHERE OwnerID=(?)", (new_count, active_id,))
        db.connection.commit()
        print("ran update")


def login_count(active_id):
    num = ([x[0] for x in db.cursor.execute("SELECT login_count FROM reports WHERE OwnerID=(?)", (active_id,))])
    return num[0]
