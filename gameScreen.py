from tkinter import *
import tkinter.font as TkFont

class Game(Frame):
    def __init__(self, parent):
        
        self.battleshipImage = PhotoImage(file="ship-set/Battleship/ShipBattleshipHull.png")
        self.carrierImage = PhotoImage(file="ship-set/Carrier/ShipCarrierHull.png")

        self.gameGrid = [[None for row in range(8)]for column in range(8)]

        Frame.__init__(self)
        self.titleFont = TkFont.Font(family="Arial", size=30, weight="bold")
        self.buttonFont = TkFont.Font(family="Arial", size=15, weight="bold")
        self.opponentCanvas = Canvas(self, width=401, height=401)
        self.opponentCanvas.grid(row=2, column=0)
        self.userCanvas = Canvas(self, width=902, height=401)
        self.userCanvas.grid(row=4, column=0)
        self.battleshipSprite = self.userCanvas.create_image(700,100, image = self.battleshipImage)
        self.carrierSprite = self.userCanvas.create_image(800, 100, image = self.carrierImage)
        self.drawOpponentGrid()
        self.rowconfigure(1, minsize=30)
        self.rowconfigure(3, minsize=50)
        self.drawUserGrid()
        self.userCanvas.bind("<ButtonRelease-1>",self.dropped)
        self.opponentCanvas.bind("<Button-1>",self.clicked)
        self.userCanvas.bind("<B1-Motion>", self.shipMoved)
        self.userCanvas.bind("<Button-1>", self.onShipClick)

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
            self.userCanvas.create_line(i+1+250,0,i+1+250,400,fill="gray")
            self.userCanvas.create_line(250,i+1,650,i+1,fill="gray")

    def dropped(self,e):
        pass

    def clicked(self,e):
        print("clicked at", e.x, e.y)
        x_result = e.x // 50
        y_result = e.y // 50
        
        print(f"row index (from 0): {x_result}")
        print(f"column index (from 0): {y_result}")
        pass

    def onShipClick(self,e):
        # sets a boundary around the image to determine if clicked
        battleshipBbox = self.userCanvas.bbox(self.battleshipSprite)
        click_x, click_y = e.x, e.y
        

        # checks if a click happens within that boundary box
        if battleshipBbox[0] < click_x < battleshipBbox[2] and battleshipBbox[1] < click_y < battleshipBbox[3]:
            print(f"Mouse clicked on the battleship!")
            self.battleshipClicked = True
        else:
            self.battleshipClicked = False

        carrierBbox = self.userCanvas.bbox(self.carrierSprite)
        click_x2, click_y2 = e.x, e.y
        # checks if a click happens within that boundary box
        if carrierBbox[0] < click_x2 < carrierBbox[2] and carrierBbox[1] < click_y2 < carrierBbox[3]:
            print(f"Mouse clicked on the carrier!")
            self.carrierClicked = True
        else:
            self.carrierClicked = False



    def shipMoved(self,e):
        print(f"x coord: {e.x}")
        print(f"y coord: {e.y}")

        if self.battleshipClicked:
            self.userCanvas.coords(self.battleshipSprite, e.x, e.y)

        if self.carrierClicked:
            self.userCanvas.coords(self.carrierSprite, e.x, e.y)
