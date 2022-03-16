import time
import tkinter as tk
import tkinter.ttk as ttk

from src.database import Database

db = Database()

BASE_FONT = ("Bookman Old Style", 10)

# global user_id to allow id to be passed between tkinter frames
user_id = None
login_count = 0


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
        # container.pack(side="top", fill="both", expand=True)
        container.grid_configure(sticky='nsew')
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Import Bookmarks", command=lambda: print("placeholder: import bookmarks"))
        filemenu.add_command(label="Export Bookmarks", command=lambda: print("placeholder: export bookmarks"))
        filemenu.add_command(label="Exit", command=quit)

        tk.Tk.config(self, menu=filemenu)

        self.frames = {}

        for F in (Login,
                  CreateNew,
                  EntryForm,
                  BookmarkAccess,
                  Reports):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Login)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        frame.event_generate('<<Raised>>')


# landing page on launch
class Login(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def login_function(event):
            if db.login_func(self.password.get(), (self.username.get())) is True:
                # controller.show_frame(EntryForm)
                controller.show_frame(Reports)
                global user_id
                user_id = db.get_user_id(self.username.get())
                global login_count
                login_count += 1
                print(login_count)
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

        self.username.bind("<Return>", login_function)
        self.password.bind("<Return>", login_function)


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

        def logout(event):
            controller.show_frame(Login)
            global user_id
            user_id = None

        def view_bookmarks(event):
            controller.show_frame(BookmarkAccess)

        def add_bookmark(event):
            if db.commit_bookmark(user_id, self.title.get(), self.link.get(), current_var.get(), ) is False:
                self.failed_commit = ttk.Label(self, text="An entry field is missing!")
                self.failed_commit.grid(row=7, column=0)
            else:
                self.title.delete(0, tk.END)
                self.link.delete(0, tk.END)
                try:
                    self.failed_commit.destroy()
                except AttributeError as e:
                    print(e)

        def add_and_update_categories(event):
            if db.add_category(user_id, current_var.get()) is False:
                self.failed_commit = ttk.Label(self, text="Category can not be added: none is entered",
                                               wraplength=120, justify='center')
                self.failed_commit.grid(row=8, column=0)
            else:
                self.category['values'] = ([x[0] for x in db.category_populate(user_id)])
                try:
                    self.failed_commit.destroy()
                except AttributeError as e:
                    print(e)

        def delete_category(event):
            db.remove_category(current_var.get())
            self.category['values'] = self.category['values'] = ([x[0] for x in db.category_populate(user_id)])

        self.title_label = ttk.Label(self, text="Title: ")
        self.title_label.grid(row=0, column=0, padx=5, pady=10)

        self.link_label = ttk.Label(self, text="Link: ")
        self.link_label.grid(row=0, column=1, padx=5, pady=10)

        self.category_label = ttk.Label(self, text="Category: ")
        self.category_label.grid(row=0, column=2, padx=5, pady=10)

        self.title = ttk.Entry(self)
        self.title.grid(row=1, column=0, padx=5, pady=10)

        self.link = ttk.Entry(self)
        self.link.grid(row=1, column=1, padx=5, pady=10)

        current_var = tk.StringVar()
        self.category = ttk.Combobox(self, textvariable=current_var)
        self.category['state'] = 'normal'
        self.category.grid(row=1, column=2, padx=5, pady=10)

        self.save_category = ttk.Button(
            self,
            text="Add New Category",
            style="my.TButton",
            command=lambda: add_and_update_categories(Login),
        )
        self.save_category.grid(row=2, column=2, padx=5, pady=10)

        self.view_bookmarks = ttk.Button(
            self,
            text="View Bookmarks",
            style="my.TButton",
            command=lambda: view_bookmarks(Login),
        )
        self.view_bookmarks.grid(row=6, column=1, padx=5, pady=10)

        self.commit_new_bookmark = ttk.Button(
            self,
            text="Add Bookmark",
            style="my.TButton",
            command=lambda: add_bookmark(Login),
        )
        self.commit_new_bookmark.grid(row=2, column=1, padx=5, pady=10)

        self.delete_category = ttk.Button(
            self,
            text="Delete Category",
            style="my.TButton",
            command=lambda: delete_category(Login),
        )
        self.delete_category.grid(row=4, column=2, padx=5, pady=10)

        self.view_reporting = ttk.Button(
            self,
            text="View Reports",
            style="my.TButton",
            command=lambda: controller.show_frame(Reports),
        )
        self.view_reporting.grid(row=6, column=0, padx=5, pady=10)

        self.logout = ttk.Button(
            self,
            text="Logout",
            style="my.TButton",
            command=lambda: logout(Login),
        )
        self.logout.grid(row=6, column=2, padx=5, pady=10)

        self.bind('<<Raised>>', self.category_pop)  # FIXME

    def category_pop(self, event=None):
        self.category['values'] = ([x[0] for x in db.category_populate(user_id)])


class BookmarkAccess(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.title_query = None

        def logout(event):
            controller.show_frame(Login)
            self.title_select.update()
            self.title_filter.delete(0, tk.END)
            global user_id
            user_id = None

        self.title_label = ttk.Label(self, text="Filter by Title: ")
        self.title_label.grid(row=0, column=0)

        # title filter: entry box
        self.title_filter = ttk.Entry(self)
        self.title_filter.grid(row=1, column=0, padx=5, pady=10)

        self.title_choices = tk.StringVar()
        self.title_select = tk.Listbox(self, listvariable=self.title_choices)
        self.title_select.grid(row=3, column=0, padx=5, pady=10, columnspan=3, sticky='WE')

        self.title_filter.bind('<Return>', self.title_filtering)

        self.title_button = ttk.Button(self, style='my.TButton', text="Filter Title",
                                       command=self.title_filtering)
        self.title_button.grid(row=2, column=0, padx=5, pady=10)

        # category filtering
        self.category_label = ttk.Label(self, text="Filter by Category: ")
        self.category_label.grid(row=0, column=2)

        self.category_var = tk.StringVar()
        self.category = ttk.Combobox(self, textvariable=self.category_var)
        self.category['state'] = 'readonly'
        self.category.grid(row=1, column=2, padx=5, pady=10)

        self.filter_category = ttk.Button(self, style='my.TButton', text="Filter by Category",
                                          command=self.category_filtering)
        self.filter_category.grid(row=2, column=2, padx=5, pady=10)

        # # link filter: combobox with the parsed sites currently in the database?
        # self.link_label = ttk.Label(self, text="Filter by Source: ")
        # self.link_label.grid(row=0, column=1)
        #
        # link_var = tk.StringVar()
        # self.link = ttk.Combobox(self, textvariable=link_var)
        #
        # def link_populate(event):
        #     self.link['values'] = db.bookmarks_by_link(user_id)  # FIXME
        #
        # self.link['state'] = 'readonly'
        # self.link.grid(row=1, column=1, padx=5, pady=10)
        #
        # link_filter = ttk.Button(self, style="my.TButton", text="Filter by Source",
        #                          command=lambda: link_populate(Login))
        # link_filter.grid(row=2, column=1, padx=5, pady=10)

        # hyperlink access
        def select_link(event):
            title = str(self.title_select.get("active")).strip("(' ',)")
            db.open_link(title)

        open_selected = ttk.Button(self, style='my.TButton', text="Open Selected",
                                   command=lambda: select_link(Login))
        open_selected.grid(row=4, column=1, padx=5, pady=10)

        def delete_bookmark(event):
            title = self.title_select.get("active")
            db.delete_bookmark(title)
            self.title_filtering()

        delete_selected = ttk.Button(self, style='my.TButton', text="Delete Selected",
                                     command=lambda: delete_bookmark(Login))
        delete_selected.grid(row=5, column=1, padx=5, pady=10)

        self.logout = ttk.Button(
            self,
            text="Logout",
            style="my.TButton",
            command=lambda: logout(Login),
        )
        self.logout.grid(row=4, column=2, padx=5, pady=10)

        self.view_reporting = ttk.Button(
            self,
            text="View Report Page",
            style="my.TButton",
            command=lambda: controller.show_frame(Reports),
        )
        self.view_reporting.grid(row=5, column=0, padx=5, pady=10)

        self.enter_bookmarks = ttk.Button(
            self,
            text="Add Bookmark Page",
            style="my.TButton",
            command=lambda: controller.show_frame(EntryForm),
        )
        self.enter_bookmarks.grid(row=4, column=0, padx=5, pady=10)

        # TODO make use of this method in each class, to get a clean refresh or update.
        self.bind('<<Raised>>', self.title_filtering, add="+")
        self.bind('<<Raised>>', self.category_pop, add="+")

    def title_filtering(self, event=None):
        self.title_query = db.bookmarks_by_title(self.title_filter.get(), user_id)
        self.title_choices.set([x[0] for x in self.title_query])

    def category_filtering(self, event=None):
        self.title_query = db.bookmarks_by_category(self.category_var.get(), user_id)
        if self.title_query:
            self.title_choices.set([x[0] for x in self.title_query])
        else:
            self.title_choices.set([x[0] for x in db.title_populate(user_id)])

    def category_pop(self, event=None):
        self.category['values'] = ([x[0] for x in db.category_populate(user_id)])


class Reports(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def logout(event):
            controller.show_frame(Login)
            global user_id
            user_id = None

        def populate_report(event):
            bvar.set(f"You have\n --{db.count_user_bookmarks(user_id)}-- \ntotal bookmarks saved!")
            lvar.set()

        self.go_entry = ttk.Button(
            self,
            text="Add Bookmarks",
            style="my.TButton",
            command=lambda: controller.show_frame(EntryForm),
        )
        self.go_entry.grid(row=0, column=0, padx=5, pady=10)

        self.view_bookmarks = ttk.Button(
            self,
            text="View Bookmarks",
            style="my.TButton",
            command=lambda: controller.show_frame(BookmarkAccess),
        )
        self.view_bookmarks.grid(row=0, column=1, padx=5, pady=10)

        self.generate_report = ttk.Button(
            self,
            text="Generate Report",
            style="my.TButton",
            command=lambda: populate_report(Login),
        )
        self.generate_report.grid(row=4, column=1, padx=5, pady=10)

        bvar = tk.StringVar()
        self.bookmark_count_label = ttk.Label(self, textvariable=bvar)
        self.bookmark_count_label.grid(row=2, column=0, padx=5, pady=10)

        lvar = tk.StringVar()
        self.login_count_label = ttk.Label(self, textvariable=lvar)
        self.login_count_label.grid(row=2, column=1, padx=5, pady=10)

        self.logout = ttk.Button(
            self,
            text="Logout",
            style="my.TButton",
            command=lambda: logout(Login),
        )
        self.logout.grid(row=4, column=0, padx=5, pady=10)


app = LoginInterface()
app.mainloop()
