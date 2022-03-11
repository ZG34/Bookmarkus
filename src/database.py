import sqlite3 as sql
import bcrypt


def hash_pw(password):
    hashed = bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt())
    password_hashed = hashed.decode('utf-8')
    return password_hashed


# Generates database and tables, and holds all queries
class Database:
    def __init__(self, *args, **kwargs):
        self.connection = sql.connect("accounts.db")
        self.cursor = self.connection.cursor()

        try:
            self.cursor.execute(
                """CREATE TABLE IF NOT EXISTS users
                (username TEXT NOT NULL, 
                password BINARY NOT NULL)
                ;"""
            )
            self.connection.commit()
        except sql.OperationalError:
            pass

        try:
            self.cursor.execute(
                """CREATE TABLE IF NOT EXISTS notes
                (OwnerID INTEGER NOT NULL,
                Data TEXT NULL)
                ;"""
            )
            self.connection.commit()
        except sql.OperationalError:
            pass

        try:
            self.cursor.execute(
                """CREATE TABLE IF NOT EXISTS category
                (OwnerID INTEGER NOT NULL,
                Data TEXT NOT NULL)
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

    def add_value(self, username, password):
        self.cursor.execute("""INSERT INTO users VALUES (?,?)""", (username, password))
        self.connection.commit()

    def check_users(self, table="users"):
        for row in self.cursor.execute(f"SELECT rowid, * FROM {table}"):
            print(row)

    def check_notes(self, active_id, table="notes"):
        for row in self.cursor.execute(f"SELECT * FROM {table} WHERE OwnerID = {active_id}"):
            print(row)

    def check_category_list(self, active_id, table="category"):
        print('checking category list')
        for row in self.cursor.execute(f"SELECT rowid, * FROM {table} WHERE OwnerID = {active_id}"):
            print(row)

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
            print(e)

    def complete_acct(self, username, password):
        if len(username) and len(password) != 0:
            self.add_value(username, (hash_pw(password)))
        else:
            return False

    def category_populate(self):
        self.cursor.execute("SELECT Data FROM category")
        return self.cursor.fetchall()

    def add_category(self, active_id, current_var):
        self.cursor.execute("INSERT INTO category (OwnerID,Data) VALUES (?,?)", (active_id, current_var,))
        self.connection.commit()

    def get_user_id(self, username):
        self.cursor.execute("SELECT rowid FROM users WHERE username = (?)", (username,))
        cleaned_id = str(self.cursor.fetchone()).strip(" ( , ) ")
        return int(cleaned_id)

    def commit_bookmark(self, active_id, title, link, category):
        self.cursor.execute("""INSERT INTO bookmarks (OwnerID,Title,Link,Category) 
        VALUES (?,?,?,?)""", (active_id, title, link, category,))
        self.connection.commit()

    def view_bookmark_table(self, active_id, table="bookmarks"):
        for row in self.cursor.execute(f"SELECT rowid, * FROM {table} WHERE OwnerID = {active_id}"):
            print(row)


if __name__ == '__main__':
    db = Database()
