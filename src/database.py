import sqlite3
import sqlite3 as sql
import bcrypt
import webbrowser


# bcrypt password hashing
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
                (username TEXT NOT NULL UNIQUE, 
                password BINARY NOT NULL)
                ;"""
            )
            self.connection.commit()
        except sql.OperationalError:
            pass

        # FIXME TESTING: Unique constraint
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
            print(e, " bad username")

    def complete_acct(self, username, password):
        if len(username) and len(password) != 0:
            try:
                self.add_value(username, (hash_pw(password)))
                print("no issue")
                return True
            except sqlite3.IntegrityError as e:
                print(e)
        else:
            print("len below 0")
            return False

    def category_populate(self, active_id):
        self.cursor.execute("SELECT Data FROM category WHERE OwnerID=(?)", (active_id,))
        # self.cursor.execute("SELECT * FROM category")
        return self.cursor.fetchall()

    def category_populate1(self):
        self.cursor.execute("SELECT Data FROM category")
        return self.cursor.fetchall()

    def add_category(self, active_id, current_var):
        if len(current_var) != 0:
            self.cursor.execute("INSERT INTO category (OwnerID,Data) VALUES (?,?)", (active_id, current_var,))
            self.connection.commit()
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

    def view_bookmark_table(self, active_id, table="bookmarks"):
        for row in self.cursor.execute(f"SELECT rowid, * FROM {table} WHERE OwnerID = {active_id}"):
            print(row)

    # fixme will not delete multi-word category
    def remove_category(self, current_var):
        self.cursor.execute("DELETE FROM category WHERE Data=(?)", (current_var,))
        self.connection.commit()

    def title_populate(self, active_id):
        self.cursor.execute("SELECT Title FROM bookmarks WHERE OwnerID = (?)", (active_id,))
        return self.cursor.fetchall()

    def open_link(self, active_selection):
        self.cursor.execute(f"SELECT Link FROM bookmarks WHERE Title=(?)", (active_selection,))
        raw = self.cursor.fetchone()[0]             # simply storing the return in a variable converts to a string?
        print(type(raw))
        webbrowser.open(raw)

    def bookmarks_by_category(self, param, active_id):
        self.cursor.execute("SELECT Title FROM bookmarks WHERE category = (?) AND OwnerID=(?)", (param, active_id))
        return self.cursor.fetchall()

    def bookmarks_by_title(self, param, active_id):
        self.cursor.execute("SELECT Title FROM bookmarks WHERE Title LIKE (?) AND OwnerID=(?)",
                            ('%'+param+'%', active_id,))
        return self.cursor.fetchall()

    def bookmarks_by_link(self, active_id):
        self.cursor.execute("SELECT Link FROM bookmarks WHERE OwnerID = (?)", (active_id,))
        raw = self.cursor.fetchall()
        return raw
        # print(raw)
        # for item in raw:
        #     print(item)
            # return item
        # print(raw)
        # return str(raw).replace("https://www.", "")
        # print(str(raw).replace("https://www.", ""))
        # slicing = slice(6)
        # print(raw[slicing])

    def bookmarks_link_populate(self, active_id):
        pass
        # pull all URLs from database
        # parse all URL for the source site (ex, www.youtube.com -> youtube)
        # select only 1 instance of each unique source site
        # populate combo box with 1 instance of each unique source site

    def bookmarks_by_link_REAL(self, choice, active_id):
        pass
        # choice =  link_var.get()
        # "SELECT Title FROM bookmarks WHERE Link LIKE (?) AND OwnerID=(?)", (choice, active_id,)

    def delete_bookmark(self, active_selection):
        self.cursor.execute("DELETE FROM bookmarks WHERE Title=(?)", (active_selection,))
        # raw = self.cursor.fetchone()[0]
        self.connection.commit()

    def print_all(self, table='category'):
        self.cursor.execute(f"SELECT * FROM {table}")
        print(self.cursor.fetchall())


if __name__ == '__main__':
    db = Database()
