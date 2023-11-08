from tkinter import *
import tkinter.font as TkFont
mainfont = ("/home/pi/Documents/q13rtaylor-project/school-project/fonts/american_captain/American Captain.ttf")

def makeDatabase(db):
    c = db.cursor()
    c.execute("DROP TABLE IF EXISTS username")
    c.execute("DROP TABLE IF EXISTS password")
    c.execute("CREATE TABLE password")
    c.execute("CREATE TABLE username (userID INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)")
    db.commit()

# initiated Class, created parameters for screens
class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.geometry("1920x1080")
        self.columnconfigure(0,weight=1)
        self.titleFont = TkFont.Font(family="Arial", size=30, weight="bold")
        self.buttonFont = TkFont.Font(family="Arial", size=15, weight="bold")


        # first screen
        self.firstFrame = Frame(self, width=1920, height=1080)
        self.title = Label(self.firstFrame, anchor="center", text="Battleships", bg="#0074b7", fg="white", font=self.titleFont)
        self.title.grid(row=0, column=0, columnspan=2, sticky="NSEW")
        self.firstFrame.columnconfigure(0,weight=1)
        self.firstFrame.rowconfigure(0,minsize=100)
        self.firstFrame.grid(row=0, column=0, columnspan=2, sticky="NSEW")
        spacing = Label(self.firstFrame, text="", height="12", width="50")
        spacing.grid(row=1, column=0, columnspan=2)

        exitButton = Button(self.firstFrame, text="Exit", height="2", width="10", command=self.destroy)
        exitButton.grid(row=0,column=1, sticky="N")

        # added interactive hover on buttons
        def changeOnHover(Button, colorOnHover, colorOnLeave):
            Button.bind("<Enter>", func=lambda e: Button.config(background=colorOnHover))
            Button.bind("<Leave>", func=lambda e: Button.config(background=colorOnLeave))


        # creating buttons
        loginButton = Button(self.firstFrame, text="Login", height="5", width="50", activebackground="#055c9d", bg="white", command = self.loginSwitch)
        loginButton.grid(row=2,column=0, columnspan=2)
        changeOnHover(loginButton, "#0074b7", "white")

        self.firstFrame.rowconfigure(3,minsize=1)

        registerButton = Button(self.firstFrame, text="Register", height="5", width="50", activebackground="#055c9d", bg="white", command=self.RegisterSwitch)
        registerButton.grid(row=4,column=0, columnspan=2)
        changeOnHover(registerButton, "#0074b7", "white")

        self.firstFrame.rowconfigure(5,minsize=1)

        guestButton = Button(self.firstFrame, text="Guest", height="5", width="50", activebackground="#055c9d", bg="white")
        guestButton.grid(row=6,column=0, columnspan=2)
        changeOnHover(guestButton, "#0074b7", "white")

        # creating other screens
        self.loginFrame = Frame(self, width=1920, height=1080)
        self.loginTitle= Label(self.loginFrame, anchor="center", text="Login", bg="#116530", fg="white", font=self.titleFont)
        self.loginTitle.grid(row=0, column=0, columnspan=2, sticky="NSEW")
        self.loginFrame.columnconfigure(0,weight=1)
        self.loginFrame.rowconfigure(0,minsize=100)

        self.loginFrame.rowconfigure(1,minsize=1)

        exitButton = Button(self.loginFrame, text="Exit", height="2", width="10", command=self.destroy)
        exitButton.grid(row=0,column=1, sticky="N")

        # back button
        backButton = Button(self.loginFrame, text="Back", height="2", width="10", activebackground="gray", activeforeground="white", command=self.BackSwitch)
        backButton.grid(row=2, column=0, columnspan=2)
        changeOnHover(backButton, "ADD8E6", "white")


        self.registerFrame = Frame(self, width=1920, height=1080)
        self.registerTitle = Label(self.registerFrame, anchor="center", text="Register", bg="#116530", fg="white", font=self.titleFont)
        self.registerTitle.grid(row=0, column=0, columnspan=2, sticky="NSEW")
        self.registerFrame.columnconfigure(0,weight=1)
        self.registerFrame.rowconfigure(0,minsize=100)

        self.registerFrame.rowconfigure(1,minsize=1)

        exitButton = Button(self.registerFrame, text="Exit", height="2", width="10", command=self.destroy)
        exitButton.grid(row=0,column=1, sticky="N")

        backButton = Button(self.registerFrame, text="Back", height="2", width="10", activebackground="gray", activeforeground="white", command=self.BackSwitch)
        backButton.grid(row=2, column=0, columnspan=2)
        changeOnHover(backButton, "ADD8E6", "white")

        self.mainloop()

    # creating way to switch between screens
    def loginSwitch(self):
        self.firstFrame.grid_forget()
        self.loginFrame.grid(row=0, column=0,rowspan=3, columnspan=2, sticky="NSEW")

    def RegisterSwitch(self):
        self.firstFrame.grid_forget()
        self.registerFrame.grid(row=0, column=0, rowspan=3, columnspan=2, sticky="NSEW")

    def BackSwitch(self):
        self.loginFrame.grid_forget()
        self.registerFrame.grid_forget()
        self.firstFrame.grid(row=0, column=0, rowspan=3, columnspan=2, sticky="NSEW")

App()