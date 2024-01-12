from tkinter import *
import tkinter.font as TkFont

class Game(Frame):
    def __init__(self, parent):

        self.battleship = PhotoImage(file="ship-set/Battleship/ShipBattleshipHull.png")

        Frame.__init__(self)
        self.titleFont = TkFont.Font(family="Arial", size=30, weight="bold")
        self.buttonFont = TkFont.Font(family="Arial", size=15, weight="bold")
        self.opponentCanvas = Canvas(self, width=401, height=401)
        self.opponentCanvas.grid(row=2, column=0)
        self.userCanvas = Canvas(self, width=401, height=401)
        self.userCanvas.grid(row=4, column=0)
        self.battleshipSprite = self.userCanvas.create_image(20,20, anchor=NE, image = self.battleship)
        self.drawOpponentGrid()
        self.rowconfigure(1, minsize=30)
        self.rowconfigure(3, minsize=50)
        self.drawUserGrid()
        self.userCanvas.bind("<Button-1>", self.grabbed)
        self.userCanvas.bind("<ButtonRelease-1>",self.dropped)
        self.opponentCanvas.bind("<Button-1>",self.clicked)

        self.title = Label(self, anchor="center", text="hello new game", bg="#0074b7", fg="white", font = self.titleFont)
        self.title.grid(row=0, column=0, sticky="NSEW", columnspan=2)
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,minsize=100)

    def drawOpponentGrid(self):
        for i in range(1,402,50):
            self.opponentCanvas.create_line(i+1,0,i+1,400,fill="gray")
            self.opponentCanvas.create_line(0,i+1,400,i+1,fill="gray")

    def drawUserGrid(self):
        for i in range(1,402,50):
            self.userCanvas.create_line(i+1,0,i+1,400,fill="gray")
            self.userCanvas.create_line(0,i+1,400,i+1,fill="gray")

    def dropped(self,e):
        pass

    def clicked(self,e):
        print("clicked at", e.x, e.y)
        x_result = e.x // 50
        y_result = e.y // 50
        

        print(f"row index (from 0): {x_result}")
        print(f"column index (from 0): {y_result}")
        pass

    def grabbed(self,e):
        pass

        #self.playerGrid = [[None for x in range(gridSize)]  for row in range(gridSize)]
        #self.opponentGrid = [[None for x in range(gridSize)]  for row in range(gridSize)]