from tkinter import *
import tkinter.font as TkFont
import time
import random
from playsound import playsound
import pickle

class Game(Frame):
    def __init__(self, parent):
        
        
        # creating user won screen
        self.wonEndFrame = Frame(width=1920, height=1080)
        self.endGameFont = TkFont.Font(family="Arial", size=30, weight="bold")
        self.endTitle = Label(self.wonEndFrame, anchor="center", text="End Game", bg="#0074b7", fg="white", font=self.endGameFont)
        self.endGameFont = TkFont.Font(family="Arial", size=30, weight="bold")
        self.endTitle.grid(row=0, column=0, sticky="NSEW", columnspan=1)
        self.spacing = Label(self.wonEndFrame, text="", height="30", width="50")
        self.spacing.grid(row=1, column=0, columnspan=2)
        self.wonTitle = Label(self.wonEndFrame, anchor="center", text="You won!", bg="green", fg="white", font=self.endGameFont)
        self.wonTitle.grid(row=3, column=0, sticky="NSEW", columnspan=1)
        self.wonEndFrame.columnconfigure(0,weight=1)
        self.wonEndFrame.rowconfigure(0,minsize=100)

        self.wonEndFrame.rowconfigure(1,minsize=1)

        # creating user lost screen
        self.lostEndFrame = Frame(width=1920, height=1080)
        self.endTitle2 = Label(self.lostEndFrame, anchor="center", text="End Game", bg="#0074b7", fg="white", font=self.endGameFont)
        self.endTitle2.grid(row=0, column=0, sticky="NSEW", columnspan=1)
        self.spacing2 = Label(self.lostEndFrame, text="", height="30", width="50")
        self.spacing2.grid(row=1, column=0, columnspan=2)
        self.lostTitle = Label(self.lostEndFrame, anchor="center", text="You lost :(", bg="red", fg="white", font=self.endGameFont)
        self.lostTitle.grid(row=3, column=0, sticky="NSEW", columnspan=1)
        self.lostEndFrame.columnconfigure(0,weight=1)
        self.lostEndFrame.rowconfigure(0,minsize=100)

        self.lostEndFrame.rowconfigure(1,minsize=1)

        

        self.battleshipImage = PhotoImage(file="ship-set/Battleship/ShipBattleshipHull.png")
        self.carrierImage = PhotoImage(file="ship-set/Carrier/ShipCarrierHull.png")

        self.splashImage = PhotoImage(file="splash.png")
        self.explosionImage = PhotoImage(file="explosion.png")

        # array initialisation
        self.userGameGrid = [[None for row in range(8)] for column in range(8)]
        self.opponentGameGrid = [[None for row in range(8)] for column in range(8)]

        self.battleshipDropBool = False
        self.carrierDropBool = False

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
        self.playGameButtonFont = TkFont.Font(family="Arial", size=25, weight="bold")
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
        # buttons creation and placing
        self.startGameButton = Button(self, text="Play Game", font=self.playGameButtonFont, command = self.startGameButtonClicked)
        self.saveGameButton = Button(self, text="Save Game", font=self.buttonFont, command=self.saveGame)
        self.saveGameButton.grid(row=2, column=0, sticky="e")
        self.loadGameButton = Button(self, text="Load Game", font=self.buttonFont, command=self.loadGame)
        self.loadGameButton.grid(row=3, column=0, sticky="e")
        self.rotateButton = Button(self, text="Rotate Ships", font=self.buttonFont, command=self.rotateShips)
        # binding different abilitties to functions
        self.rotateButton.grid(row=4, column=0, pady=10, padx=600, sticky="w")
        self.userCanvas.bind("<ButtonRelease-1>",self.shipDropped)
        self.opponentCanvas.bind("<Button-1>",self.clicked)
        self.userCanvas.bind("<B1-Motion>", self.shipMoved)
        self.rotateButton.bind("<Button-1>", self.rotateShips)
        self.userCanvas.bind("<Button-1>", self.onShipClick)

        self.title = Label(self, anchor="center", text="Battleships", bg="#0074b7", fg="white", font = self.titleFont)
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
            self.battleshipDropBool = True
        else:
            self.carrierDropped(e)
            self.carrierDropBool = True

        if self.battleshipDropBool and self.carrierDropBool == True:
            self.startGameButton.grid(row=4, column=0, sticky="e")

    def startGameButtonClicked(self):
        self.turn()

    def battleshipDropped(self,e):
        if self.battleshipClicked:
            self.battleshipCoords = self.userCanvas.coords(self.battleshipSprite)
        row = int((self.battleshipCoords[1] - 250) // 50)
        col = int((self.battleshipCoords[0] - 250) // 50)

        global snappedCol
        global snappedRow
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

        global snappedCol2
        global snappedRow2
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

    def hitUserShipSegment(self, row, col, x_coord, y_coord):
        if self.opponentTurn == True:
            shipName = ""

            if self.userGameGrid[row][col] is None:
                print("Opponent shot missed")
                self.userCanvas.create_image((x_coord)+250, (y_coord), image = self.splashImage, anchor="nw")
                self.update()
                #playsound('cannon_miss.mp3')
            
            if self.userGameGrid[row][col] is not None and self.userGameGrid[row][col][0] == 1:
                shipName = "Battleship"
                self.userBattleshipSegments -=1
                self.userCanvas.create_image((x_coord)+250, (y_coord), image = self.explosionImage, anchor="nw")
                self.update()
                print(f"Opponent hit the {shipName}")
                self.userShipHit = True
                self.userGameGrid[row][col] = None

            if self.userGameGrid[row][col] is not None and self.userGameGrid[row][col][0] == 2:
                shipName = "Carrier"
                self.userCarrierSegments -=1
                self.userCanvas.create_image((x_coord)+250, (y_coord), image = self.explosionImage, anchor="nw")
                self.update()
                print(f"Opponent hit the {shipName}")
                self.userShipHit = True
                self.userGameGrid[row][col] = None

            if self.userBattleshipSegments == 0:
                print("User Battleship Destroyed!")

            elif self.userCarrierSegments == 0:
                print("User Carrier destroyed!")

            if self.userCarrierSegments == 0 and self.userBattleshipSegments == 0:
                Frame.grid_forget(self)
                self.lostEndFrame.grid(row=0, column=0, rowspan=3, columnspan=2, sticky="NSEW")

            self.userTurn = True
            self.opponentTurn = False
            print("")
            print("User's turn")
            print("")

    def hitOpponentShipSegment(self, row, col):
        if self.userTurn == True:
            shipName = ""

            if self.opponentGameGrid[row][col] is None:
                print("User shot missed")
                print("")
                self.opponentCanvas.create_image((row*50), (col*50), image = self.splashImage, anchor="nw")
                self.update()
                #playsound('cannon_miss.mp3')
            
            if self.opponentGameGrid[row][col] == "battleship":
                shipName = "Battleship"
                self.opponentBattleshipSegments -=1
                self.opponentCanvas.create_image((row*50), (col*50), image = self.explosionImage, anchor="nw")
                self.update()
                print(f"User hit the {shipName}")
                self.opponentGameGrid[row][col] = None

            if self.opponentGameGrid[row][col] == "carrier":
                shipName = "Carrier"
                self.opponentCarrierSegments -=1
                self.opponentCanvas.create_image((row*50), (col*50), image = self.explosionImage, anchor="nw")
                self.update()
                print(f"User hit the {shipName}")
                self.opponentGameGrid[row][col] = None

            if self.opponentBattleshipSegments == 0:
                print("")
                print("Opponent Battleship Destroyed!")
                print("")
                print(self.opponentGameGrid)

            if self.opponentCarrierSegments == 0:
                print("")
                print("Opponent Carrier destroyed!")
                print("")
                print(self.opponentGameGrid)

            if self.opponentCarrierSegments == 0 and self.opponentBattleshipSegments == 0:
                Frame.grid_forget(self)
                self.wonEndFrame.grid(row=0, column=0, rowspan=3, columnspan=2, sticky="NSEW")

            self.opponentTurn = True
            self.userTurn = False
            print("")
            print("Opponent's turn")
            print("")
            self.opponentClicked()

    def opponentClicked(self):
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

            self.hitUserShipSegment(x_result, y_result, x_coord, y_coord)

    def clicked(self, e):
        print("clicked at", e.x, e.y)
        x_result = e.x // 50
        y_result = e.y // 50
        
        print(f"row index (from 0): {x_result}")
        print(f"column index (from 0): {y_result}")

        self.hitOpponentShipSegment(x_result, y_result)
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

    def turn(self):
        print("Opponent's turn")
        self.opponentTurn = True
        self.opponentClicked()

    def saveGame(self):
        file1 = open("userSaveFile.pickle", "wb")
        file2 = open("opponentSaveFile.pickle", "wb")
        file3 = open("battleshipRow.pickle", "wb")
        file4 = open("battleshipCol.pickle", "wb")
        file5 = open("carrierRow.pickle", "wb")
        file6 = open("carrierCol.pickle", "wb")

        pickle.dump(self.userGameGrid, file1)
        pickle.dump(self.opponentGameGrid, file2)
        pickle.dump(snappedRow, file3)
        pickle.dump(snappedCol, file4)
        pickle.dump(snappedRow2, file5)
        pickle.dump(snappedCol2, file6)

        file1.close()
        file2.close()
        file3.close()
        file4.close()
        file5.close()
        file6.close()

        print("Saved Game Successfully")

    def loadGame(self):
        file1 = open("userSaveFile.pickle", "rb")
        file2 = open("opponentSaveFile.pickle", "rb")
        file3 = open("battleshipRow.pickle", "rb")
        file4 = open("battleshipCol.pickle", "rb")
        file5 = open("carrierRow.pickle", "rb")
        file6 = open("carrierCol.pickle", "rb")

        self.userGameGrid = pickle.load(file1)
        self.opponentGameGrid = pickle.load(file2)

        battleshipOldRow = pickle.load(file3)
        battleshipOldCol = pickle.load(file4)
        self.userCanvas.coords(self.battleshipSprite, battleshipOldCol, battleshipOldRow)

        carrierOldRow = pickle.load(file5)
        carrierOldCol = pickle.load(file6)
        self.userCanvas.coords(self.carrierSprite, carrierOldCol, carrierOldRow)
        self.startGameButton.grid(row=4, column=0, sticky="e")
        self.update()

        file1.close()
        file2.close()
        file3.close()
        file4.close()
        file5.close()
        file6.close()
        print("Loaded Game Successfully")

    # DEVELOPMENT PRIORITIES
        # add an end game when all ships are destroyed
        # add a counter to the side of the grids, how many ships left each

    # TO FIX
        # opponents ships on it's grid can overlap
        # opponent's clicks are off when hitting the ships