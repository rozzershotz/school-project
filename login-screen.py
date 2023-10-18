from tkinter import *
import tkinter.font as TkFont
mainfont = ("/home/pi/Documents/q13rtaylor-project/school-project/fonts/american_captain/American Captain.ttf")

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
        self.title = Label(self.firstFrame, anchor="center", text="Battleships", bg="blue", fg="white", font=self.titleFont)
        self.title.grid(row=0, column=0, sticky="NSEW")
        self.firstFrame.columnconfigure(0,weight=1)
        self.firstFrame.rowconfigure(0,minsize=100)
        self.firstFrame.grid(row=0, column=0, sticky="NSEW")
        spacing = Label(self.firstFrame, text="", height="12", width="50")
        spacing.grid(row=1, column=0)

        # added interactive hover on buttons
        def changeOnHover(Button, colorOnHover, colorOnLeave):
            Button.bind("<Enter>", func=lambda e: Button.config(background=colorOnHover))
    
            Button.bind("<Leave>", func=lambda e: Button.config(background=colorOnLeave))

        # creating buttons
        loginButton = Button(self.firstFrame, text="Login", height="5", width="50", activebackground="blue", activeforeground="white", command = self.loginSwitch)
        loginButton.grid(row=2,column=0)
        changeOnHover(loginButton, "#ADD8E6", "white")

        self.firstFrame.rowconfigure(3,minsize=1)

        registerButton = Button(self.firstFrame, text="Register", height="5", width="50", activebackground="blue", activeforeground="white", command=self.RegisterSwitch)
        registerButton.grid(row=4,column=0)
        changeOnHover(registerButton, "#ADD8E6", "white")

        self.firstFrame.rowconfigure(5,minsize=1)

        guestButton = Button(self.firstFrame, text="Guest", height="5", width="50", activebackground="gray", activeforeground="white")
        guestButton.grid(row=6,column=0)
        changeOnHover(guestButton, "#ADD8E6", "white")

        # creating other screens
        self.loginFrame = Frame(self, width=1920, height=1080)
        self.loginTitle= Label(self.loginFrame, anchor="center", text="Login", bg="green", fg="white", font=self.titleFont)
        self.loginTitle.grid(row=0, column=0, sticky="NSEW")
        self.loginFrame.columnconfigure(0,weight=1)
        self.loginFrame.rowconfigure(0,minsize=100)

        self.loginFrame.rowconfigure(1,minsize=1)

        # back button
        backButton = Button(self.loginFrame, text="Back", height="2", width="10", activebackground="gray", activeforeground="white", command=self.BackSwitch)
        backButton.grid(row=2, column=0)
        changeOnHover(backButton, "ADD8E6", "white")


        self.registerFrame = Frame(self, width=1920, height=1080)
        self.registerTitle = Label(self.registerFrame, anchor="center", text="Register", bg="green", fg="white", font=self.titleFont)
        self.registerTitle.grid(row=0, column=0, sticky="NSEW")
        self.registerFrame.columnconfigure(0,weight=1)
        self.registerFrame.rowconfigure(0,minsize=100)

        self.registerFrame.rowconfigure(1,minsize=1)

        backButton = Button(self.registerFrame, text="Back", height="2", width="10", activebackground="gray", activeforeground="white", command=self.BackSwitch)
        backButton.grid(row=2, column=0)
        changeOnHover(backButton, "ADD8E6", "white")

        self.mainloop()

    # creating way to switch between screens
    def loginSwitch(self):
        self.firstFrame.grid_forget()
        self.loginFrame.grid(row=0, column=0,rowspan=3, sticky="NSEW")

    def RegisterSwitch(self):
        self.firstFrame.grid_forget()
        self.registerFrame.grid(row=0, column=0, rowspan=3, sticky="NSEW")

    def BackSwitch(self):
        self.loginFrame.grid_forget()
        self.registerFrame.grid_forget()
        self.firstFrame.grid(row=0, column=0, rowspan=3, sticky="NSEW")

App()