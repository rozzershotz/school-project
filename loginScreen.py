from tkinter import *
import tkinter.font as TkFont
from gameScreen import Game
import sqlite3
from tkinter import messagebox as ms

mainfont = ("/home/pi/Documents/q13rtaylor-project/school-project/fonts/american_captain/American Captain.ttf")

# creates database (if not created already)
with sqlite3.connect('userdatabase.db') as db:
    c = db.cursor()

c.execute('CREATE TABLE IF NOT EXISTS user (username TEXT NOT NULL PRIMARY KEY,password TEXT NOT NULL);')
db.commit()
db.close()

# initiated Class, created parameters for screens
class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.geometry("1280x720")
        self.columnconfigure(0,weight=1)
        self.titleFont = TkFont.Font(family="Arial", size=30, weight="bold")
        self.buttonFont = TkFont.Font(family="Arial", size=15, weight="bold")

        self.userSoundChoice = True

        # database global variables
        self.username = StringVar()
        self.password = StringVar()
        self.n_username = StringVar()
        self.n_password = StringVar()
        self.username_delete = StringVar()
        self.head = None

        # Sets up the database
        self.db2 = None
        # Holds database information
        self.db = None
        self.db_connection()

    # Open Database connection
    def db_connection(self):
        with sqlite3.connect('userdatabase.db') as self.db2:
            self.db = self.db2.cursor()

    # Close Database connection
    def db_close_connection(self):
        self.db.close()

    def login(self):
        # Establish Connection
        # Moved to db_connection()
        # Find user, if there is any take proper action
        find_user = 'SELECT * FROM user WHERE username = ? and password = ?'
        self.db.execute(find_user, [(self.username.get()), (self.password.get())])
        result = self.db.fetchall()
        if result:
            ms.showinfo("Success!", f"{self.username.get()} Logged In Successfully")
            self.loginFrame.grid_forget()
            self.mainMenuFrame.grid(row=0, column=0, rowspan=3, columnspan=2, sticky="NSEW")

        else:
            ms.showerror('Oops!', 'Username Not Found.')

    def new_user(self):
        # Establish Connection
        # Moved to db_connection()

        # Find Existing username, if any take proper action
        find_user = 'SELECT username FROM user WHERE username = ?'
        self.db.execute(find_user, [(self.n_username.get())])

        if self.db.fetchall():
            ms.showerror('Error!', 'Username Taken Try a Different One.')

        else:
            ms.showinfo('Success!', 'Account Created!')

        # Create New Account
        insert = 'INSERT INTO user(username,password) VALUES(?,?)'
        self.db.execute(insert, [(self.n_username.get()), (self.n_password.get())])
        self.db2.commit()
        
    def delete_user(self):
        # Check if the username exists
        find_user = 'SELECT username FROM user WHERE username = ?'
        self.db.execute(find_user, [(self.username_delete.get())])

        if not self.db.fetchall():
            ms.showerror('Error!', 'User not found.')

        else:
            # Delete the user
            delete_query = 'DELETE FROM user WHERE username = ?'
            self.db.execute(delete_query, [(self.username_delete.get())])
            self.db2.commit()
            ms.showinfo('Success!', 'User deleted successfully.')

    def run(self):
        # first screen
        self.gamescreen = Game(self)
        self.firstFrame = Frame(self, width=1920, height=1080)
        self.title = Label(self.firstFrame, anchor="center", text="Battleships", bg="#0074b7", fg="white", font=self.titleFont)
        self.title.grid(row=0, column=0, sticky="NSEW", columnspan=2)
        self.firstFrame.columnconfigure(0,weight=1)
        self.firstFrame.rowconfigure(0,minsize=100)
        self.firstFrame.grid(row=0, column=0, columnspan=2, sticky="NSEW")
        spacing = Label(self.firstFrame, text="", height="12", width="50")
        spacing.grid(row=1, column=0, columnspan=2)

        self.addExitButton(self.firstFrame)


        # creating buttons
        loginButton = Button(self.firstFrame, text="Login", height="5", width="50", background = "white", activebackground="#055c9d", activeforeground="white", command = self.loginSwitch)
        loginButton.grid(row=2,column=0, columnspan=2)
        self.changeOnHover(loginButton, "#0074b7", "white")

        self.firstFrame.rowconfigure(3,minsize=1)

        registerButton = Button(self.firstFrame, text="Register", height="5", width="50", background = "white", activebackground="#055c9d", activeforeground="white", command=self.RegisterSwitch)
        registerButton.grid(row=4,column=0, columnspan=2)
        self.changeOnHover(registerButton, "#0074b7", "white")

        self.firstFrame.rowconfigure(5,minsize=1)   

        guestButton = Button(self.firstFrame, text="Guest", height="5", width="50", background = "white", activebackground="#055c9d", activeforeground="white", command = self.mainMenuSwitch)
        guestButton.grid(row=6,column=0, columnspan=2)
        self.changeOnHover(guestButton, "#0074b7", "white")


        # creating other screens
        self.loginFrame = Frame(self, width=1920, height=1080)
        self.loginTitle = Label(self.loginFrame, anchor="center", text="Login", bg="#116530", fg="white", font=self.titleFont)
        self.loginTitle.grid(row=0, column=0, sticky="NSEW", columnspan=2)
        self.loginFrame.columnconfigure(0,weight=1)
        self.loginFrame.rowconfigure(0,minsize=100)

        self.loginFrame.rowconfigure(1,minsize=1)

        self.addBackButton(self.loginFrame)
        Label(self.loginFrame, text='Username: ', font=('', 20)).grid(sticky=W, padx=600)
        Entry(self.loginFrame, textvariable=self.username, bd=2, font=self.buttonFont).grid(row=2, column=0, columnspan=2)
        Label(self.loginFrame, text='Password: ', font=('', 20)).grid(sticky=W, padx=600)
        Entry(self.loginFrame, textvariable=self.password, bd=2, font=self.buttonFont, show='*').grid(row=3, column=0, columnspan=2)

        Button(self.loginFrame, text=' Login ', bd=3, font=self.buttonFont, padx=5, pady=5, command=self.login).grid(columnspan=2)

        Label(self.loginFrame, text='Delete User: ', font=('', 20)).grid(sticky=W, padx=600)
        Entry(self.loginFrame, textvariable=self.username_delete, bd=2, font=self.buttonFont).grid(row=5, column=0, columnspan=2)
        Button(self.loginFrame, text=' Delete ', bd=3, font=self.buttonFont, padx=5, pady=5, command=self.delete_user).grid(columnspan=2)

        self.addExitButton(self.loginFrame)

        self.registerFrame = Frame(self, width=1920, height=1080)
        self.registerTitle = Label(self.registerFrame, anchor="center", text="Register", bg="#116530", fg="white", font=self.titleFont)
        self.registerTitle.grid(row=0, column=0, sticky="NSEW", columnspan=2)
        self.registerFrame.columnconfigure(0,weight=1)
        self.registerFrame.rowconfigure(0,minsize=100)

        self.registerFrame.rowconfigure(1,minsize=1)

        self.addExitButton(self.registerFrame)
        Label(self.registerFrame, text='Username: ', font=('', 20)).grid(row=2, sticky=W, padx=600)
        Entry(self.registerFrame, textvariable=self.n_username, bd=2, font=self.buttonFont).grid(row=3, column=0, columnspan=2)
        Label(self.registerFrame, text='Password: ', font=('', 20)).grid(sticky=W, padx=600)
        Entry(self.registerFrame, textvariable=self.n_password, bd=2, font=self.buttonFont, show='*').grid(row=4, column=0, columnspan=2)

        Button(self.registerFrame, text='Create Account', bd=3, font=self.buttonFont, padx=5, pady=5, command=self.new_user).grid(columnspan=2)
        Button(self.registerFrame, text='Go to Login', bd=3, font=self.buttonFont, padx=5, pady=5, command=self.loginSwitch).grid(columnspan=2)

        self.addBackButton(self.registerFrame)

        self.mainMenuFrame = Frame(self, width=1920, height=1080)
        self.mainTitle = Label(self.mainMenuFrame, anchor="center", text="Main Menu", bg="#116530", fg="white", font=self.titleFont)
        self.mainTitle.grid(row=0, column=0, sticky="NSEW", columnspan=2)
        self.mainMenuFrame.columnconfigure(0,weight=1)
        self.mainMenuFrame.rowconfigure(0,minsize=100)
        spacing2 = Label(self.mainMenuFrame, text="", height="10", width="50")
        spacing2.grid(row=2, column=0, columnspan=2)

        self.settingsFrame = Frame(self, width=1920, height=1080)
        self.settingsTitle = Label(self.settingsFrame, anchor="center", text="Settings", bg="#915F6D", fg="white", font=self.titleFont)
        self.settingsTitle.grid(row=0, column=0, sticky="NSEW", columnspan=2)
        self.settingsFrame.columnconfigure(0,weight=1)
        self.settingsFrame.rowconfigure(0,minsize=100)
        self.settingsFrame.rowconfigure(1,minsize=1)

        self.soundToggle = Button(self.settingsFrame, text="On", width=12, relief="raised", bg="#116530", bd=3, font=self.buttonFont, padx=5, pady=5, command=self.toggle)
        Label(self.settingsFrame, text='Sound: ', font=('', 20)).grid(row=3, sticky=W, padx=600)
        self.soundToggle.grid(row=3, column=0, columnspan=2, pady=10)

        self.addMainMenuBack(self.settingsFrame)
        self.addExitButton(self.settingsFrame)

        playButton = Button(self.mainMenuFrame, text="Play", height="5", width="50", background = "white", activebackground="#055c9d", activeforeground="white", command = self.launchGame)
        playButton.grid(row=3,column=0, columnspan=2)
        self.changeOnHover(playButton, "#0074b7", "white")

        achievementButton = Button(self.mainMenuFrame, text="Achievements", height="5", width="50", background = "white", activebackground="#055c9d", activeforeground="white")
        achievementButton.grid(row=4,column=0, columnspan=2)
        self.changeOnHover(achievementButton, "#0074b7", "white")

        settingsButton = Button(self.mainMenuFrame, text="Settings", height="5", width="50", background = "white", activebackground="#055c9d", activeforeground="white", command=self.settingsSwitch)
        settingsButton.grid(row=5,column=0, columnspan=2)
        self.changeOnHover(settingsButton, "#0074b7", "white")

        self.mainMenuFrame.rowconfigure(1,minsize=1)

        self.addExitButton(self.mainMenuFrame)
        self.addBackButton(self.mainMenuFrame)

        self.mainloop()

    # added interactive hover on buttons
    def changeOnHover(self, Button, colorOnHover, colorOnLeave):
        Button.bind("<Enter>", func=lambda e: Button.config(background=colorOnHover))
        Button.bind("<Leave>", func=lambda e: Button.config(background=colorOnLeave))

    def addBackButton(self, frameRef):
        backButton = Button(frameRef, text="Back", height="2", width="10", background = "white", activebackground="gray", activeforeground="white", command=self.BackSwitch)
        backButton.grid(row=1, column=0, columnspan=2, pady=10)
        self.changeOnHover(backButton, "#ADD8E6", "white")

    def addExitButton(self, frameRef):
        exitButton = Button(frameRef, text="Quit", height="2", width="10", background = "white", activebackground="gray", activeforeground="white", command=self.destroy)
        exitButton.grid(row=0, column=1)
        self.changeOnHover(exitButton, "#ADD8E6", "white")

    def addMainMenuBack(self, frameRef):
        backButton = Button(frameRef, text="Back", height="2", width="10", background = "white", activebackground="gray", activeforeground="white", command=self.mainMenuBackSwitch)
        backButton.grid(row=1, column=0, columnspan=2, pady=10)
        self.changeOnHover(backButton, "#ADD8E6", "white")

    def toggle(self):
        if self.soundToggle.config('relief')[-1] == 'sunken':
            self.soundToggle.config(relief="raised", bg="red", text="Off", fg="white")
            self.userSoundChoice = False
        else:
            self.soundToggle.config(relief="sunken")
            self.soundToggle.config(bg="#116530", text="On", fg="white")
            self.userSoundChoice = True

    # creating way to switch between screens
    def loginSwitch(self):
        self.firstFrame.grid_forget()
        self.registerFrame.grid_forget()
        self.loginFrame.grid(row=0, column=0,rowspan=3, columnspan=2, sticky="NSEW")

    def RegisterSwitch(self):
        self.firstFrame.grid_forget()
        self.registerFrame.grid(row=0, column=0, rowspan=3, columnspan=2, sticky="NSEW")

    def BackSwitch(self):
        self.loginFrame.grid_forget()
        self.registerFrame.grid_forget()
        self.mainMenuFrame.grid_forget()
        self.firstFrame.grid(row=0, column=0, rowspan=3, columnspan=2, sticky="NSEW")

    def mainMenuBackSwitch(self):
        self.settingsFrame.grid_forget()
        self.mainMenuFrame.grid(row=0, column=0, rowspan=3, columnspan=2, sticky="NSEW")

    def mainMenuSwitch(self):
        self.firstFrame.grid_forget()
        self.mainMenuFrame.grid(row=0, column=0, rowspan=3, columnspan=2, sticky="NSEW")

    def launchGame(self):
        self.mainMenuFrame.grid_forget()
        self.gamescreen.setUserSoundChoice(self.userSoundChoice)
        self.gamescreen.grid(row=0, column=0, rowspan=3, columnspan=2, sticky="NSEW")

    def settingsSwitch(self):
        self.mainMenuFrame.grid_forget()
        self.settingsFrame.grid(row=0, column=0, rowspan=3, columnspan=2, sticky="NSEW")


app = App()
app.run()