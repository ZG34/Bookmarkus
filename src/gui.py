import tkinter as tk
import tkinter.ttk as ttk

from src.database import Database

db = Database()

BASE_FONT = ("Bookman Old Style", 10)

# global user_id to allow id to be passed between tkinter frames
user_id = None


# contains tkinter setup logic, to allow for switching frames
class LoginInterface(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        button_styling = ttk.Style()
        button_styling.configure("my.TButton", font=BASE_FONT)

        label_styling = ttk.Style()
        label_styling.configure("my.TLabel", font=BASE_FONT)

        tk.Tk.wm_title(self, "Login Screen")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (Login,
                  CreateNew,
                  EntryForm,
                  BookmarkAccess):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Login)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# landing page on launch
class Login(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def login_function(event):
            if db.login_func(self.password.get(), (self.username.get())) is True:
                controller.show_frame(EntryForm)
                global user_id
                user_id = db.get_user_id(self.username.get())
                self.password.delete(0, tk.END)
                try:
                    self.label3.destroy()
                except AttributeError:
                    pass
            else:
                self.label3.grid(row=6, column=2)

        self.label0 = ttk.Label(self, text="Login Interface")
        self.label0.grid(row=0, column=0, padx=40, pady=10)

        self.label1 = ttk.Label(self, text="Username: ", style="my.TLabel")
        self.label1.grid(row=1, column=1)

        self.username = ttk.Entry(self)
        self.username.grid(row=1, column=2)

        self.label2 = ttk.Label(self, text="Password: ", style="my.TLabel")
        self.label2.grid(row=2, column=1, pady=10)

        self.password = ttk.Entry(self, show="*")
        self.password.grid(row=2, column=2, pady=10)

        self.label3 = ttk.Label(self, text="Incorrect account info")

        self.login = ttk.Button(
            self, text="Login", style="my.TButton", command=lambda: login_function(Login)
        )
        self.login.grid(row=3, column=2)

        self.create_new = ttk.Button(
            self,
            text="Create New Account",
            style="my.TButton",
            command=lambda: controller.show_frame(CreateNew),
        )
        self.create_new.grid(row=4, column=2, pady=10)

        # self.username.bind("<Return>", login_func)
        # self.password.bind("<Return>", login_func)


# account creation page
class CreateNew(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def create_account(event):
            if db.complete_acct(self.username.get(), self.password.get()) is True:
                self.username.delete(0, tk.END), self.password.delete(0, tk.END)
                self.done = ttk.Label(self, text="account created", style="my.TLabel")
                self.done.grid(row=5, column=1)
            elif db.complete_acct(self.username.get(), self.password.get()) is False:
                self.failed = ttk.Label(
                    self, text="missing info", style="my.TLabel"
                )
                self.failed.grid(row=5, column=1)
            else:
                self.failed = ttk.Label(
                    self, text="name taken", style="my.TLabel"
                )
                self.failed.grid(row=5, column=1)

        self.label0 = ttk.Label(self, text="New Account")
        self.label0.grid(row=0, column=0, padx=40, pady=10)

        self.label1 = ttk.Label(self, text="Set Username:", style="my.TLabel")
        self.label1.grid(row=1, column=1)
        self.username = ttk.Entry(self)
        self.username.grid(row=1, column=2)

        self.label2 = ttk.Label(self, text="Set Password:", style="my.TLabel")
        self.label2.grid(row=2, column=1, padx=5, pady=5)
        self.password = ttk.Entry(self)
        self.password.grid(row=2, column=2)

        self.create_button = ttk.Button(
            self,
            text="Complete New Account",
            style="my.TButton",
            command=lambda: create_account(Login),
        )
        self.create_button.grid(row=3, column=2, padx=5, pady=5)

        self.checkDB = ttk.Button(
            self, text="test DB", style="my.TButton", command=lambda: db.check_users()
        )
        self.checkDB.grid(row=4, column=2)

        self.home = ttk.Button(
            self,
            text="Go to Login",
            style="my.TButton",
            command=lambda: controller.show_frame(Login),
        )
        self.home.grid(row=5, column=2, padx=5, pady=5)


# bookmark entry page
class EntryForm(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def add_bookmark(event):
            db.commit_bookmark(user_id, self.title.get(), self.link.get(), current_var.get(), )
            self.title.delete(0, tk.END)
            self.link.delete(0, tk.END)

        def add_and_update_categories(event):
            db.add_category(user_id, current_var.get())
            self.category['values'] = db.category_populate()  # refreshes combobox contents

        def delete_category(event):
            db.remove_category(current_var.get())
            self.category['values'] = db.category_populate()

        self.title_label = ttk.Label(self, text="Title: ")
        self.title_label.grid(row=0, column=0)

        self.link_label = ttk.Label(self, text="Link: ")
        self.link_label.grid(row=0, column=1)

        self.category_label = ttk.Label(self, text="Category: ")
        self.category_label.grid(row=0, column=2)

        self.title = ttk.Entry(self)
        self.title.grid(row=1, column=0, padx=5, pady=10)

        self.link = ttk.Entry(self)
        self.link.grid(row=1, column=1, padx=5, pady=10)

        current_var = tk.StringVar()
        self.category = ttk.Combobox(self, textvariable=current_var)
        self.category['values'] = db.category_populate()
        self.category['state'] = 'normal'
        self.category.grid(row=1, column=2, padx=5, pady=10)

        self.save_category = ttk.Button(
            self,
            text="Add New Category",
            style="my.TButton",
            command=lambda: add_and_update_categories(Login),
        )
        self.save_category.grid(row=2, column=2)

        # self.view_category_list = ttk.Button(
        #     self,
        #     text="View Category List",
        #     style="my.TButton",
        #     command=lambda: db.check_category_list(user_id),
        # )
        # self.view_category_list.grid(row=3, column=2)

        self.view_bookmarks = ttk.Button(
            self,
            text="View Bookmarks",
            style="my.TButton",
            # command=lambda: db.view_bookmark_table(user_id),
            command=lambda: controller.show_frame(BookmarkAccess),
        )
        self.view_bookmarks.grid(row=3, column=1)

        self.commit_new_bookmark = ttk.Button(
            self,
            text="Add Bookmark",
            style="my.TButton",
            command=lambda: add_bookmark(Login),
        )
        self.commit_new_bookmark.grid(row=4, column=1)

        self.delete_category = ttk.Button(
            self,
            text="Delete Selected",
            style="my.TButton",
            command=lambda: delete_category(Login),
        )
        self.delete_category.grid(row=4, column=2)

        self.home = ttk.Button(
            self,
            text="Go to Login",
            style="my.TButton",
            command=lambda: controller.show_frame(Login),
        )
        self.home.grid(row=5, column=2)


class BookmarkAccess(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.title_label = ttk.Label(self, text="Filter by Title: ")
        self.title_label.grid(row=0, column=0)

        # title filter: entry box
        title_filter = ttk.Entry(self)
        title_filter.grid(row=1, column=0, padx=5, pady=10)

        # title select, listbox
        title_query = db.title_populate()
        title_choices = tk.StringVar(value=title_query)
        title_select = tk.Listbox(self, listvariable=title_choices)
        title_select.grid(row=2, column=0, padx=5, pady=10)

        # hyperlink access
        def select_link(event):
            title = str(title_select.get("active")).strip("(' ',)")
            db.open_link(title)

        open_selected = ttk.Button(self, style='my.TButton', text="Open Selected",
                                   command=lambda: select_link(Login))
        open_selected.grid(row=3, column=0)

        # ability to filter the listbox: by title, by link source, by category
        # filtering by link source will require parsing between www. and .site

        # category filter will be a combobox, with typing in new categories disabled

        # link filter: combobox with the parsed sites currently in the database?

        # RUNNER: how will I run this filter? by section or entirely at once?
        # how can I accept empty fields, and how can I combine multiple fields?


app = LoginInterface()
app.mainloop()
