# BookMarkus
A tool for creating and storing bookmarks on the local machine. 

Aside from the actual functionality - the goal of this project was to learn a few new tools, work on project and code structure,
and explore some ideas. 

<img src="https://i.gyazo.com/321e7cb44ecf63a3ca9b9015ac662557.png" width="300">
<img src="https://i.gyazo.com/bc7a258c3e2bfe1f4ae368a210c20659.png" width="300">
<img src="https://i.gyazo.com/b90deeab5d190585ccf75f0156757528.png" width="300">
<img src="https://i.gyazo.com/3e8e94788ed155c7c18b870ab49ec180.png" width="300">


## Features
* Account creation & verification to access user-specific bookmarks, with hashed & salted passwords.
* Simple reporting on usage per user.
* Ability to add bookmarks with a title, a link, and a category.
* Ability to view, filter, access, and delete all stored bookmarks.


## Tools Used
* bcrypt - password security (salted & hashed, verified on login)
* sqlite3 - CRUD operations, with tables for: user accounts, categories, bookmarks, and reporting.
* tkinter - GUI


### Learning Points
#### *first time using any database, as well as bcrypt*
* Next project, I am going to focus on test driven development and proper testing. As my largest project so far, I was running
into issues and side effects a bit more than I had in other projects. As I understand it, testing can help with this.
All tests in this project were done manually, with print() and type() statements. 
* For future projects of similar structure, I may look to split files more often to maintain better organization. I began
to split the database methods up into specific files near the end of this project. Generally look to continue improving project
and code structure.


### Known Bugs
* Using the logout button on certain frames will result in the label popups in **class Login** frame to not populate on new
login attempts (no issue with actual login).
* Some combination of creating new accounts + logging in may result in database locking on **def login_function**.
* just a note, not a bug: as the local db file and actual bookmarks are not hashed or encrypted, the data is not actually secure.