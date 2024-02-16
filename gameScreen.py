from tkinter import *
import tkinter.font as TkFont
import time
import random
from playsound import playsound 

class Game(Frame):
    def __init__(self, parent):
        
        self.battleshipImage = PhotoImage(file="ship-set/Battleship/ShipBattleshipHull.png")
        self.carrierImage = PhotoImage(file="ship-set/Carrier/ShipCarrierHull.png")

        self.splashImage = PhotoImage(file="splash.png")

        self.userGameGrid = [[None for row in range(8)] for column in range(8)]
        self.opponentGameGrid = [[None for row in range(8)] for column in range(8)]

        self.userBattleshipSegments = 4
        self.userCarrierSegments = 4

        self.opponentBattleshipSegments = 4
        self.opponentCarrierSegments = 4

        self.userShipHit = False

        self.userTurn = False
        self.opponentTurn = False

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

        self.placeOpponentShips()

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

        if self.userGameGrid[row][col] is not None and self.battleshipClicked:
            self.userCanvas.coords(self.battleshipSprite, 700, 100)
        if col < 0 or col > 400:
            self.userCanvas.coords(self.battleshipSprite, 700, 100)
            return

        print("battleship dropped at: ", row, col)
        if self.battleshipClicked:
            print(self.userCanvas.coords(self.battleshipSprite))
            self.userCanvas.coords(self.battleshipSprite, snappedCol, snappedRow)
            self.userGameGrid[row][col] = (self.battleshipSprite, 1)
            self.userGameGrid[row+1][col] = (self.battleshipSprite, 2)
            self.userGameGrid[row+2][col] = (self.battleshipSprite, 3)
            self.userGameGrid[row+3][col] = (self.battleshipSprite, 4)

            print(self.userGameGrid)
            print(f"battleship snapped to: row - {str(snappedRow)} column - {str(snappedCol)}")

    def carrierDropped(self, e):
        if self.carrierClicked:
            self.carrierCoords = self.userCanvas.coords(self.carrierSprite)
        row = int((self.carrierCoords[1] - 250) // 50)
        col = int((self.carrierCoords[0] - 250) // 50)

        snappedCol2 = 250 + col * 50
        snappedRow2 = 250 + row * 50

        if self.userGameGrid[row][col] is not None and self.carrierClicked:
            self.userCanvas.coords(self.carrierSprite, 800, 100)
        if col < 0 or col > 400:
            self.userCanvas.coords(self.carrierSprite, 800, 100)
            return

        print("carrier dropped at: ", row, col)
        if self.carrierClicked:
            print(self.userCanvas.coords(self.carrierSprite))
            self.userCanvas.coords(self.carrierSprite, snappedCol2, snappedRow2)
            self.userGameGrid[row][col] = (self.carrierSprite, 1)
            self.userGameGrid[row+1][col] = (self.carrierSprite, 2)
            self.userGameGrid[row+2][col] = (self.carrierSprite, 3)
            self.userGameGrid[row+3][col] = (self.carrierSprite, 4)

            print(self.userGameGrid)
            print(self.opponentGameGrid)
            print(str(snappedCol2))

            self.turn(e)

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
                    if self.userGameGrid[col][row] is not None and self.userGameGrid[col][row][0] == self.battleshipSprite:
                        self.userGameGrid[col][row] = None
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
                    if self.userGameGrid[col][row] is not None and self.userGameGrid[col][row][0] == self.carrierSprite:
                        self.userGameGrid[col][row] = None
        else:
            self.carrierClicked = False


    def shipMoved(self,e):
        print(f"x coord: {e.x}")
        print(f"y coord: {e.y}")

        if self.battleshipClicked:
            self.userCanvas.coords(self.battleshipSprite, e.x, e.y)

        if self.carrierClicked:
            self.userCanvas.coords(self.carrierSprite, e.x, e.y)

    def rotateShips(self, e):
        click_x, click_y = e.x, e.y
        if self.battleshipClicked:
            self.rotateShip(self.battleshipSprite)
        elif self.carrierClicked:
            self.rotateShip(self.carrierSprite)

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
            self.userGameGrid[row][col] = (shipSprite, 1)
            self.userGameGrid[row][col + 1] = (shipSprite, 2)
            self.userGameGrid[row][col + 2] = (shipSprite, 3)
            self.userGameGrid[row][col + 3] = (shipSprite, 4)
        elif shipSprite == self.carrierSprite:
            self.userGameGrid[row][col] = (shipSprite, 1)
            self.userGameGrid[row + 1][col] = (shipSprite, 2)
            self.userGameGrid[row + 2][col] = (shipSprite, 3)
            self.userGameGrid[row + 3][col] = (shipSprite, 4)

    def hitUserShipSegment(self, row, col, e):
        if self.opponentTurn == True:
            shipName = ""

            if self.userGameGrid[row][col] is None:
                print("Opponent shot missed")
                self.userCanvas.create_image(row, col, image = self.splashImage)
                playsound('cannon_miss.mp3')
                self.userTurn = True
                self.opponentTurn = False
            
            if self.userGameGrid[row][col][0] == 1:
                shipName = "Battleship"
                self.userBattleshipSegments -=1
            else:
                shipName = "Carrier"
                self.userCarrierSegments -=1

            self.userGameGrid[row][col] = None
            print(f"Opponent hit the {shipName}")

            self.userShipHit = True

            if self.userBattleshipSegments == 0:
                print("User Battleship Destroyed!")

            elif self.userCarrierSegments == 0:
                print("User Carrier destroyed!")

            self.userTurn = True
            self.opponentTurn = False

    def hitOpponentShipSegment(self, row, col, e):
        if self.userTurn == True:
            shipName = ""

            if self.opponentGameGrid[row][col] is None:
                print("User shot missed")
                self.opponentCanvas.create_image(row, col, image = self.splashImage)
                playsound('cannon_miss.mp3')
                
                self.opponentTurn = True
                self.userTurn = False
                self.opponentClicked(e)
            
            if self.opponentGameGrid[row][col] == "battleship":
                shipName = "Battleship"
                self.opponentBattleshipSegments -=1
            else:
                shipName = "Carrier"
                self.opponentCarrierSegments -=1

            self.opponentGameGrid[row][col] = None
            print(f"User hit the {shipName}")

            if self.opponentBattleshipSegments == 0:
                print("Opponent Battleship Destroyed!")

            elif self.userCarrierSegments == 0:
                print("Opponent Carrier destroyed!")

            self.opponentTurn = True
            self.userTurn = False
            self.opponentClicked(e)


    def opponentClicked(self, e):
            time.sleep(3)
            x_coord = random.randrange(0, 400, 50)
            y_coord = random.randrange(0, 400, 50)
            print(f"opponent clicked at {x_coord}, {y_coord}")
            x_result = x_coord // 50
            y_result = y_coord // 50

            if self.userShipHit == True:
                x_choice_1 = x_coord - 50
                x_choice_2 = x_coord + 50

                y_choice_1 = y_coord - 50
                y_choice_2 = y_coord + 50

                choice = [x_choice_1, x_choice_2]
                x_coord = random.choice(choice)

                choice2 = [y_choice_1, y_choice_2]
                y_coord = random.choice(choice2)

                x_result = x_coord // 50
                y_result = y_coord // 50
            
            print(f"row index (from 0): {x_result}")
            print(f"column index (from 0): {y_result}")

            self.hitUserShipSegment(x_result, y_result, e)

    def clicked(self, e):
        print("clicked at", e.x, e.y)
        x_result = e.x // 50
        y_result = e.y // 50
        
        print(f"row index (from 0): {x_result}")
        print(f"column index (from 0): {y_result}")

        self.hitOpponentShipSegment(x_result, y_result, e)
        pass

    def placeOpponentShips(self):
    # Place Battleship randomly
        battleship_row = random.randint(0, 7)
        battleship_col = random.randint(0, 3)
        for i in range(4):
            self.opponentGameGrid[battleship_row][battleship_col + i] = "battleship"

        # Place Carrier randomly
        carrier_row = random.randint(0, 3)
        carrier_col = random.randint(0, 7)
        for i in range(4):
            self.opponentGameGrid[carrier_row + i][carrier_col] = "carrier"

    def turn(self, e):
        for col in range(8):
                for row in range(8):
                    if 1 or 2 == self.userGameGrid[row][col][0]:
                        time.sleep(3)
                        answer = input("Ready to play? - Y/N: ")
                        if answer == "Y":
                            print("Opponent's turn")
                            self.opponentTurn = True
                            self.opponentClicked(e)



    # DEVELOPMENT PRIORITIES
        # get random placing of ships on opponent grid (DONE)
        # add a turn system
        # add animations to screen for diff things (splashes and explosions)
        # add a counter to the side of the grids, how many ships left each
        # add an end game screen (win/lose kinda thing)