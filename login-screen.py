from tkinter import *
import tkinter.font as TkFont
mainfont = ("/home/pi/Documents/q13rtaylor-project/school-project/fonts/american_captain/American Captain.ttf")

class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.geometry("1920x1080")
        self.columnconfigure(0,weight=1)
        self.titleFont = TkFont.Font(family="Arial", size=20)
        self.buttonFont = TkFont.Font(family="Arial", size=15)

        self.firstFrame = Frame(self, width=1920, height=1080)
        self.title = Label(self.firstFrame, anchor="center", text="Login, Register, or Continue as Guest", bg="blue", fg="white", font=self.titleFont)
        self.title.grid(row=0, column=0, sticky="NSEW")
        self.firstFrame.columnconfigure(0,weight=1)
        self.firstFrame.rowconfigure(0,minsize=100)
        b1=Button(self.firstFrame, text="Login", height="5", width="50")
        b1.grid(row=1,column=0)
        self.firstFrame.grid(row=0, column=0, sticky="NSEW")

        self.mainloop()

App()