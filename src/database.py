import sqlite3
import sqlite3 as sql
import bcrypt
import webbrowser
from src.pwtesting import password_check


# bcrypt password hashing
def hash_pw(password):
    hashed = bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt())
    password_hashed = hashed.decode('utf-8')
    return password_hashed


# Generates database and tables, and holds account creation +  bookmarking queries
class Database:
    def __init__(self, *args, **kwargs):
        self.connection = sql.connect("accounts.db")
        self.cursor = self.connection.cursor()

        try:
            self.cursor.execute(
                """CREATE TABLE IF NOT EXISTS users
                (username TEXT NOT NULL UNIQUE, 
                password BINARY NOT NULL)
                ;"""
            )
            self.connection.commit()
        except sql.OperationalError:
            pass

        try:
            self.cursor.execute(
                """CREATE TABLE IF NOT EXISTS category
                (OwnerID INTEGER NOT NULL,
                Data TEXT NOT NULL UNIQUE)
                ;"""
            )
            self.connection.commit()
        except sql.OperationalError:
            pass

        try:
            self.cursor.execute(
                """CREATE TABLE IF NOT EXISTS bookmarks
                (OwnerID INTEGER NOT NULL,
                Title TEXT NOT NULL,
                Link TEXT NOT NULL,
                Category TEXT NOT NULL)
                ;"""
            )
            self.connection.commit()
        except sql.OperationalError:
            pass

    def login_func(self, password, username):
        self.cursor.execute("SELECT password FROM users WHERE username = (?)", (username,))
        result = str(self.cursor.fetchone()).strip("'(),")
        b_result = bytes(result, 'utf-8')
        try:
            if bcrypt.checkpw(bytes(password, 'utf-8'), b_result):
                print('validated')
                return True
            else:
                print("failed validation")
        except ValueError as e:
            print(e, " bad username")

    def add_value(self, username, password):
        self.cursor.execute("""INSERT INTO users VALUES (?,?)""", (username, password))
        self.connection.commit()

    def complete_acct(self, username, password):
        if len(username) and len(password) != 0:
            if password_check(password) is True:
                try:
                    self.add_value(username, (hash_pw(password)))
                    self.connection.commit()
                    print("no issue")
                    return True
                except sqlite3.IntegrityError as e:
                    print(e)
            else:
                return 0
        else:
            print("len below 0")
            return False

    def category_populate(self, active_id):
        self.cursor.execute("SELECT Data FROM category WHERE OwnerID=(?)", (active_id,))
        return self.cursor.fetchall()

    def add_category(self, active_id, current_var):
        if len(current_var) != 0:
            try:
                self.cursor.execute("INSERT INTO category (OwnerID,Data) VALUES (?,?)", (active_id, current_var,))
                self.connection.commit()
            except sqlite3.IntegrityError as e:
                print(e)
        else:
            print("please enter a category")
            return False

    def get_user_id(self, username):
        self.cursor.execute("SELECT rowid FROM users WHERE username = (?)", (username,))
        cleaned_id = str(self.cursor.fetchone()).strip(" ( , ) ")
        return int(cleaned_id)

    def commit_bookmark(self, active_id, title, link, category):
        if len(title) and len(link) != 0:
            self.cursor.execute("""INSERT INTO bookmarks (OwnerID,Title,Link,Category) 
            VALUES (?,?,?,?)""", (active_id, title, link, category,))
            self.connection.commit()
        else:
            print("nothing to bookmark")
            return False

    def remove_category(self, current_var):
        self.cursor.execute("DELETE FROM category WHERE Data=(?)", (current_var,))
        self.connection.commit()

    def title_populate(self, active_id):
        self.cursor.execute("SELECT Title FROM bookmarks WHERE OwnerID = (?)", (active_id,))
        return self.cursor.fetchall()

    def open_link(self, active_selection):
        self.cursor.execute(f"SELECT Link FROM bookmarks WHERE Title=(?)", (active_selection,))
        raw = self.cursor.fetchone()[0]             # simply storing the return in a variable converts to a string?
        webbrowser.open(raw)

    def bookmarks_by_category(self, param, active_id):
        self.cursor.execute("SELECT Title FROM bookmarks WHERE category = (?) AND OwnerID=(?)", (param, active_id))
        return self.cursor.fetchall()

    def bookmarks_by_title(self, param, active_id):
        self.cursor.execute("SELECT Title FROM bookmarks WHERE Title LIKE (?) AND OwnerID=(?)",
                            ('%'+param+'%', active_id,))
        return self.cursor.fetchall()

    def delete_bookmark(self, active_selection):
        self.cursor.execute("DELETE FROM bookmarks WHERE Title=(?)", (active_selection,))
        self.connection.commit()


if __name__ == '__main__':
    db = Database()
