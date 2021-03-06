import sys
import tkinter as tk
import tkinter.ttk as ttk

from src.database import Database
import src.reporting as report
import src.export as export

report.report_table()
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

        tk.Tk.wm_title(self, "BookMarkus")

        container = tk.Frame(self)
        container.grid_configure(sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(
            label="Export Bookmarks", command=lambda: export.export_bookmarks(user_id)
        )
        filemenu.add_command(label="Exit", command=sys.exit)

        tk.Tk.config(self, menu=filemenu)

        self.frames = {}

        for F in (Login, CreateNew, EntryForm, BookmarkAccess, Reports):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Login)

    # method for raising new pages (frames)
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        frame.event_generate("<<Raised>>")


# landing page on launch
class Login(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def login_function(event):
            if db.login_func(self.password.get(), (self.username.get())) is True:
                controller.show_frame(Reports)
                global user_id
                user_id = db.get_user_id(self.username.get())
                login_count = 1
                report.login_logging(user_id, login_count)
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
            self,
            text="Login",
            style="my.TButton",
            command=lambda: login_function(Login),
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

        def home(event):
            controller.show_frame(Login)
            try:
                self.done.destroy()
                self.failed.destroy()
            except AttributeError as e:
                pass

        def create_account(event):
            if db.complete_acct(self.username.get(), self.password.get()) is True:
                try:
                    self.failed.destroy()
                    self.done.destroy()
                except AttributeError as e:
                    pass
                self.username.delete(0, tk.END), self.password.delete(0, tk.END)
                self.done = ttk.Label(self, text="account created", style="my.TLabel")
                self.done.grid(row=5, column=1)
            elif db.complete_acct(self.username.get(), self.password.get()) is False:
                try:
                    self.failed.destroy()
                    self.done.destroy()
                except AttributeError as e:
                    pass
                self.failed = ttk.Label(self, text="missing info", style="my.TLabel")
                self.failed.grid(row=5, column=1)
            elif db.complete_acct(self.username.get(), self.password.get()) == 0:
                try:
                    self.failed.destroy()
                    self.done.destroy()
                except AttributeError as e:
                    pass
                self.failed = ttk.Label(self, text="bad password", style="my.TLabel")
                self.failed.grid(row=5, column=1)
            else:
                try:
                    self.failed.destroy()
                    self.done.destroy()
                except AttributeError as e:
                    pass
                self.failed = ttk.Label(self, text="name taken", style="my.TLabel")
                self.failed.grid(row=5, column=1)

        self.pw_reqs = ttk.Label(
            self,
            text="Password Requirements:\n"
                 "-- between 6 and 20 characters long\n"
                 "-- must have at least 1 uppercase and 1 lowercase\n"
                 "-- must have at least 1 number and 1 special character",
        )
        self.pw_reqs.grid(row=6, column=0, columnspan=2)

        self.done = ttk.Label(self)
        self.failed = ttk.Label(self)

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
            command=lambda: home(Login),
        )
        self.home.grid(row=5, column=2, padx=5, pady=5)


# bookmark entry page
class EntryForm(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def cleanup():
            try:
                self.title.delete(0, tk.END)
                self.link.delete(0, tk.END)
                self.category.delete(0, tk.END)
            except AttributeError as e:
                pass

        def logout(event):
            controller.show_frame(Login)
            global user_id
            user_id = None
            cleanup()

        def view_bookmarks(event):
            controller.show_frame(BookmarkAccess)
            cleanup()

        def add_bookmark(event):
            add_and_update_categories(Login)
            if (
                    db.commit_bookmark(
                        user_id,
                        self.title.get(),
                        self.link.get(),
                        current_var.get(),
                    )
                    is False
            ):
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
                self.failed_commit = ttk.Label(
                    self,
                    text="Category can not be added: none is entered",
                    wraplength=120,
                    justify="center",
                )
                self.failed_commit.grid(row=8, column=0)
            else:
                self.category["values"] = [x[0] for x in db.category_populate(user_id)]
                try:
                    self.failed_commit.destroy()
                except AttributeError as e:
                    pass

        def delete_category(event):
            db.remove_category(current_var.get())
            self.category["values"] = self.category["values"] = [
                x[0] for x in db.category_populate(user_id)
            ]

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
        self.category["state"] = "normal"
        self.category.grid(row=1, column=2, padx=5, pady=10)

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
        self.commit_new_bookmark.grid(
            row=2, column=0, padx=5, pady=10, columnspan=3, sticky="ew"
        )

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

        self.bind("<<Raised>>", self.category_pop)  # FIXME

    def category_pop(self, event=None):
        self.category["values"] = [x[0] for x in db.category_populate(user_id)]


# view, filter, and access bookmarks
class BookmarkAccess(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def cleanup():
            try:
                self.title_filter.delete(0, tk.END)
                self.title_select.update()
                self.category_var = tk.StringVar()
            except AttributeError as e:
                pass

        self.title_query = None

        def logout(event):
            controller.show_frame(Login)
            global user_id
            user_id = None
            cleanup()

        def delete_bookmark(event):
            title = self.title_select.get("active")
            db.delete_bookmark(title)
            self.title_filtering()

        # hyperlink access
        def select_link(event):
            title = str(self.title_select.get("active")).strip("(' ',)")
            db.open_link(title)
            bookmark_open_count = 1
            report.access_logging(user_id, bookmark_open_count)

        def page_add_bookmarks(event):
            controller.show_frame(EntryForm)
            cleanup()

        def page_view_reports(event):
            controller.show_frame(Reports)
            cleanup()

        self.title_label = ttk.Label(self, text="Filter by Title: ")
        self.title_label.grid(row=0, column=0)

        self.title_filter = ttk.Entry(self)
        self.title_filter.grid(row=1, column=0, padx=5, pady=10)

        self.title_choices = tk.StringVar()
        self.title_select = tk.Listbox(self, listvariable=self.title_choices)
        self.title_select.grid(
            row=3, column=0, padx=5, pady=10, columnspan=3, sticky="WE"
        )

        self.title_filter.bind("<Return>", self.title_filtering)

        self.category_label = ttk.Label(self, text="Filter by Category: ")
        self.category_label.grid(row=0, column=2)

        self.category_var = tk.StringVar()
        self.category = ttk.Combobox(self, textvariable=self.category_var)
        self.category["state"] = "readonly"
        self.category.grid(row=1, column=2, padx=5, pady=10)

        open_selected = ttk.Button(
            self,
            style="my.TButton",
            text="Open Selected",
            command=lambda: select_link(Login),
        )
        open_selected.grid(row=4, column=1, padx=5, pady=10)

        delete_selected = ttk.Button(
            self,
            style="my.TButton",
            text="Delete Selected",
            command=lambda: delete_bookmark(Login),
        )
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
            command=lambda: page_view_reports(Login),
        )
        self.view_reporting.grid(row=5, column=0, padx=5, pady=10)

        self.enter_bookmarks = ttk.Button(
            self,
            text="Add More Bookmarks",
            style="my.TButton",
            command=lambda: page_add_bookmarks(Login),
        )
        self.enter_bookmarks.grid(row=4, column=0, padx=5, pady=10)

        self.bind("<<Raised>>", self.title_filtering, add="+")
        self.bind("<<Raised>>", self.category_pop, add="+")
        self.category.bind("<<ComboboxSelected>>", self.category_filtering)
        self.title_filter.bind("<KeyRelease>", lambda event, arg=0: self.title_searcher(self.title_filter))

    def title_searcher(self, entrywidget):
        active_value = entrywidget.get()
        self.title_query = db.bookmarks_by_title(active_value, user_id)
        self.title_choices.set([x[0] for x in self.title_query])

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
        self.category["values"] = [x[0] for x in db.category_populate(user_id)]


# landing page after login, allows all other pages to be viewed as well as a simple report to be generated
class Reports(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def logout(event):
            controller.show_frame(Login)
            # resets all labels to be blank, preparing for next user to log in
            logoutvar = tk.StringVar()
            self.bookmark_count_label.config(textvariable=logoutvar)
            self.login_count_label.config(textvariable=logoutvar)
            self.open_count_label.config(textvariable=logoutvar)
            global user_id
            user_id = None

        def populate_report(event):
            # configs are here to reset labels to accept the proper variables, after a logout
            self.bookmark_count_label.config(textvariable=bvar)
            self.login_count_label.config(textvariable=lvar)
            self.open_count_label.config(textvariable=ovar)
            bvar.set(
                f"You have\n --{report.count_user_bookmarks(user_id)}-- \ntotal bookmarks"
            )
            lvar.set(f"Logged in\n --{report.login_count(user_id)}-- \ntotal times")
            ovar.set(f"Accessed bookmarks\n --{report.show_access(user_id)}-- \ntimes")

        self.go_entry = ttk.Button(
            self,
            text="Add Bookmarks",
            style="my.TButton",
            command=lambda: controller.show_frame(EntryForm),
        )
        self.go_entry.grid(row=0, column=0, padx=5, pady=10, columnspan=2, sticky="ew")

        self.view_bookmarks = ttk.Button(
            self,
            text="View Bookmarks",
            style="my.TButton",
            command=lambda: controller.show_frame(BookmarkAccess),
        )
        self.view_bookmarks.grid(
            row=1, column=0, padx=5, pady=10, columnspan=2, sticky="ew"
        )

        self.generate_report = ttk.Button(
            self,
            text="Generate Report",
            style="my.TButton",
            command=lambda: populate_report(Login),
        )
        self.generate_report.grid(
            row=4, column=0, padx=5, pady=10, columnspan=3, sticky="ew"
        )

        bvar = tk.StringVar()
        self.bookmark_count_label = ttk.Label(
            self,
            textvariable=bvar,
            borderwidth=1,
            relief="ridge",
            anchor="center",
            width=20,
        )
        self.bookmark_count_label.grid(
            row=2, column=0, padx=5, pady=10, ipadx=3, ipady=3
        )

        lvar = tk.StringVar()
        self.login_count_label = ttk.Label(
            self,
            textvariable=lvar,
            borderwidth=1,
            relief="ridge",
            anchor="center",
            width=20,
        )
        self.login_count_label.grid(row=2, column=1, padx=5, pady=10, ipadx=3, ipady=3)

        ovar = tk.StringVar()
        self.open_count_label = ttk.Label(
            self,
            textvariable=ovar,
            borderwidth=1,
            relief="ridge",
            anchor="center",
            width=20,
        )
        self.open_count_label.grid(row=2, column=2, padx=5, pady=10, ipadx=3, ipady=3)

        self.logout = ttk.Button(
            self,
            text="Logout",
            style="my.TButton",
            command=lambda: logout(Login),
        )
        self.logout.grid(row=5, column=1, padx=5, pady=10)


app = LoginInterface()
app.resizable(False, False)
app.mainloop()
