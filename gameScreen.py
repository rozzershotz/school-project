from tkinter import *
import tkinter.font as TkFont

class Game(Frame):
    def __init__(self, parent):
        Frame.__init__(self)
        self.titleFont = TkFont.Font(family="Arial", size=30, weight="bold")
        self.buttonFont = TkFont.Font(family="Arial", size=15, weight="bold")

        self.title = Label(self, anchor="center", text="hello new game", bg="#0074b7", fg="white", font = self.titleFont)
        self.title.grid(row=0, column=0, sticky="NSEW", columnspan=2)
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,minsize=100)

        spacing = Label(self, text="", height="12", width="50")
        spacing.grid(row=1, column=0, columnspan=2)

        #self.playerGrid = [[None for x in range(gridSize)]  for row in range(gridSize)]
        #self.opponentGrid = [[None for x in range(gridSize)]  for row in range(gridSize)]