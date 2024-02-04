from tkinter import *
import tkinter.font as TkFont

class Game(Frame):
    def __init__(self, parent):
        
        self.battleshipImage = PhotoImage(file="ship-set/Battleship/ShipBattleshipHull.png")
        self.carrierImage = PhotoImage(file="ship-set/Carrier/ShipCarrierHull.png")

        self.gameGrid = [[None for row in range(8)] for column in range(8)]

        Frame.__init__(self)
        self.titleFont = TkFont.Font(family="Arial", size=30, weight="bold")
        self.buttonFont = TkFont.Font(family="Arial", size=15, weight="bold")
        self.opponentCanvas = Canvas(self, width=401, height=401)
        self.opponentCanvas.grid(row=2, column=0)
        self.userCanvas = Canvas(self, width=902, height=401)
        self.userCanvas.grid(row=4, column=0)
        self.battleshipSprite = self.userCanvas.create_image(700,100, image = self.battleshipImage, anchor="nw")
        self.carrierSprite = self.userCanvas.create_image(800, 100, image = self.carrierImage, anchor="nw")
        self.drawOpponentGrid()
        self.rowconfigure(1, minsize=30)
        self.rowconfigure(3, minsize=50)
        self.drawUserGrid()
        self.rotateButton = Button(self, text="Rotate Ships", command=self.rotateShips, font=self.buttonFont)
        self.rotateButton.grid(row=4, column=0, pady=10, padx=600, sticky="w")
        self.userCanvas.bind("<ButtonRelease-1>",self.shipDropped)
        self.opponentCanvas.bind("<Button-1>",self.clicked)
        self.userCanvas.bind("<B1-Motion>", self.shipMoved)
        self.rotateButton.bind("<Button-1>", self.rotateShips)
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

    def shipDropped(self, e):
        if self.battleshipClicked:
            self.battleshipDropped(e)
        else:
            self.carrierDropped(e)
        

    def battleshipDropped(self,e):
        if self.battleshipClicked:
            self.battleshipCoords = self.userCanvas.coords(self.battleshipSprite)
        row = int((self.battleshipCoords[1] - 250) // 50)
        col = int((self.battleshipCoords[0] - 250) // 50)

        snappedCol = 250 + col * 50
        snappedRow = 250 + row * 50

        # seeing if cell is already occupied
        if self.gameGrid[row][col] is not None and self.battleshipClicked:
            self.userCanvas.coords(self.battleshipSprite, 700, 100)
        if col < 0 or col > 400:
            self.userCanvas.coords(self.battleshipSprite, 700, 100)
            return
        
        print("battleship dropped at: ", row, col)
        if self.battleshipClicked:
            print(self.userCanvas.coords(self.battleshipSprite))

            self.userCanvas.coords(self.battleshipSprite, snappedCol, snappedRow)
            self.gameGrid[row][col] = (self.battleshipSprite, 1)
            self.gameGrid[row][col+1] = (self.battleshipSprite, 2)
            self.gameGrid[row][col+2] = (self.battleshipSprite, 3)
            self.gameGrid[row][col+3] = (self.battleshipSprite, 4)

            print(self.gameGrid)

    def carrierDropped(self, e):
        if self.carrierClicked:
            self.carrierCoords = self.userCanvas.coords(self.carrierSprite)
        row = int((self.carrierCoords[1] - 250) // 50)
        col = int((self.carrierCoords[0] - 250) // 50)

        snappedCol2 = 250 + col * 50
        snappedRow2 = 250 + row * 50

        if self.gameGrid[row][col] is not None and self.carrierClicked:
            self.userCanvas.coords(self.carrierSprite, 800, 100)
        if col < 0 or col > 400:
            self.userCanvas.coords(self.carrierSprite, 800, 100)
            return

        print("carrier dropped at: ", row, col)
        if self.carrierClicked:
            print(self.userCanvas.coords(self.carrierSprite))
            self.userCanvas.coords(self.carrierSprite, snappedCol2, snappedRow2)
            self.gameGrid[row][col] = (self.carrierSprite, 1)
            self.gameGrid[row][col+1] = (self.carrierSprite, 2)
            self.gameGrid[row][col+2] = (self.carrierSprite, 3)
            self.gameGrid[row][col+3] = (self.carrierSprite, 4)

            print(self.gameGrid)

    def clicked(self, e):
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
            for col in range(8):
                for row in range(8):
                    if self.gameGrid[col][row] is not None and self.gameGrid[col][row][0] == self.battleshipSprite:
                        self.gameGrid[col][row] = None
        else:
            self.battleshipClicked = False

        carrierBbox = self.userCanvas.bbox(self.carrierSprite)
        click_x2, click_y2 = e.x, e.y
        
        # checks if a click happens within that boundary box
        if carrierBbox[0] < click_x2 < carrierBbox[2] and carrierBbox[1] < click_y2 < carrierBbox[3]:
            print(f"Mouse clicked on the carrier!")
            self.carrierClicked = True
            for col in range(8):
                for row in range(8):
                    if self.gameGrid[col][row] is not None and self.gameGrid[col][row][0] == self.carrierSprite:
                        self.gameGrid[col][row] = None
        else:
            self.carrierClicked = False


    def shipMoved(self,e):
        print(f"x coord: {e.x}")
        print(f"y coord: {e.y}")

        if self.battleshipClicked:
            self.userCanvas.coords(self.battleshipSprite, e.x, e.y)

        if self.carrierClicked:
            self.userCanvas.coords(self.carrierSprite, e.x, e.y)

    def rotateShips(self, e=None):
        self.battleshipClicked = True
        self.carrierClicked = True
        if self.battleshipClicked:
            self.rotateShip(self.battleshipSprite, self.e)
        elif self.carrierClicked:
            self.rotateShip(self.carrierSprite, self.e)

    def rotateShip(self, shipSprite):
        currentCoords = self.userCanvas.coords(shipSprite)

        if len(currentCoords) < 4:
            return

        centerX = (currentCoords[0] + currentCoords[2]) / 2
        centerY = (currentCoords[1] + currentCoords[3]) / 2

        rotatedCoords = [centerX - (centerY - self.e.y), centerY + (centerX - self.e.x), centerX + (centerY - self.e.y), centerY - (centerX - self.e.x)]

        # Update canvas coordinates
        self.userCanvas.coords(shipSprite, *rotatedCoords)

        # Update gameGrid array
        row = int((rotatedCoords[1] - 250) // 50)
        col = int((rotatedCoords[0] - 250) // 50)

        if shipSprite == self.battleshipSprite:
            self.gameGrid[row][col] = (shipSprite, 1)
            self.gameGrid[row][col + 1] = (shipSprite, 2)
            self.gameGrid[row][col + 2] = (shipSprite, 3)
            self.gameGrid[row][col + 3] = (shipSprite, 4)
        elif shipSprite == self.carrierSprite:
            self.gameGrid[row][col] = (shipSprite, 1)
            self.gameGrid[row + 1][col] = (shipSprite, 2)
            self.gameGrid[row + 2][col] = (shipSprite, 3)
            self.gameGrid[row + 3][col] = (shipSprite, 4)