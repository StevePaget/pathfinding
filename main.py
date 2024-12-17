from tkinter import *
import tkinter.font as tkFont
from copy import deepcopy
import math
import heapq


class Walker():
    def __init__(self, cellx,celly, canvas):
        
        self.cellx = cellx
        self.celly = celly
        self.angle = 0
        self.images = []
        for i in range(0,4):
            self.images.append(PhotoImage(file="walker" + str(i) + ".png"))
        self.imageID  = canvas.create_image(self.cellx*30, self.celly*30, image=self.images[0], anchor = "nw")
        self.target = (19,19)
        self.path = None

    def performAStar(self, gameGrid, walkers, changed, canvas):
        current = (self.celly, self.cellx)
        if current == self.target:
            return False
        if changed:
            self.starGrid = [[ None for _ in range(20)] for _ in range(20)]
            heuristic =  self.getHeuristic(self.cellx, self.celly)
            #                                         total,     Visited   path       heuristic    From
            self.starGrid[self.celly][self.cellx] = [  heuristic, True,     0,        heuristic,   None]
            self.border = []
            heapq.heappush(self.border, self.starGrid[self.celly][self.cellx])
            while current != (19,19):
                thisCell = self.starGrid[current[0]][current[1]]
                self.starGrid[current[0]][current[1]][0] = True
                # look at unvisited neighbours of current
                directions = [(-1,0), (0,1), (1,0), (0,-1)]
                for dy,dx in directions:
                    neighboury = current[0]+dy
                    neighbourx = current[1]+dx
                    if 0<= neighbourx <=19 and 0<= neighboury<=19: # it's on the grid
                        neighbourCell =self.starGrid[neighboury][neighbourx]
                        if neighbourCell !="X": # it's not a blocked out cell
                            if neighbourCell is None:  # it's never been seen
                                self.border.append((neighboury,neighbourx)) # stick it in the border
                                newPath = thisCell[1]+1
                                newheuristic = self.getHeuristic(neighbourx, neighboury)
                                self.starGrid[neighboury][neighbourx] = [False, newPath,  newheuristic, newPath+newheuristic,  current]
                            elif neighbourCell[0] is not True: # it's not visited
                                # check this cell's path and update values
                                newPath = thisCell[1]+1
                                newTotal = newPath + neighbourCell[2]
                                if  newTotal <  neighbourCell[3]:
                                    self.starGrid[neighboury][neighbourx] = [False,  newPath,  neighbourCell[2], newTotal, current ]
            
                # now find the shortest total in the border
                bestTotal = math.inf
                bestLocation = None
                #print("Border now ",self.border)
                for location in self.border:
                    thisCell = self.starGrid[location[0]][location[1]]
                    #print(location, thisCell)
                    if thisCell[0] is False and thisCell[3] < bestTotal:
                        bestTotal = thisCell[3]
                        bestLocation = location
                current = bestLocation
            # track back
            self.path = [self.starGrid[current[0]][current[1]][4]]
            while current != (self.celly, self.cellx):
                self.path.append(current)
                current = self.starGrid[current[0]][current[1]][4]
        self.celly, self.cellx = self.path[-1]
        canvas.coords(self.imageID, self.cellx*30, self.celly*30)
        return True
                


    def getHeuristic(self,x,y):
        return math.sqrt((self.target[0]-x)**2 + (self.target[1]-y)**2)


    
class Block():
    def __init__(self, x,y, canvas):    
        self.image = PhotoImage(file="block.png")
        self.imageID  = canvas.create_image(x, y, image=self.image, anchor = "center")

    def drag(self,x,y, canvas):
        canvas.coords(self.imageID, x, y)

class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.titlefont = tkFont.Font(family="Arial", size=34, slant="italic")
        self.buttonfont = tkFont.Font(family="Courier", size=18)
        self.geometry("1000x700")
        self.title("A* Walkers")

        self.canvas = Canvas(self, width=900, height=700, bg="lightgreen")
        self.canvas.grid(row=0,column=0, rowspan=5)
        self.canvas.bind("<ButtonRelease-1>", self.stopDraw)
        self.canvas.bind("<Motion>", self.draw)
        self.canvas.bind("<Button-1>", self.startDraw)
        self.canvas.bind("<Button-3>", self.erase)
        
        self.drawGrid()
        self.drawing = False
        self.drawActive = False
        runButton = Button(self,text="Run", command=self.run)
        runButton.grid(row=0,column=1)
        self.drawButton = Button(self,text="Draw", command=self.DrawOn)
        self.drawButton.grid(row=1,column=1)
        self.walkers = []
        self.changed = True

        self.gameGrid = [ [None for row in range(20)] for col in range(20)]
        self.star = PhotoImage(file="star.png")
        self.canvas.create_image(19*30,19*30,image=self.star, anchor="nw")
        self.running = False
        self.mainloop() # must be last thing in the initialisation.

    def run(self):
        if not self.running:
            self.running = True
            self.performAStar()
        else:
            self.running = False

    def DrawOn(self):
        if not self.drawActive:
            self.drawActive = True
            self.drawButton.configure(text="Stop")
        else:
            self.drawActive = False
            self.drawButton.configure(text="Draw")

    def performAStar(self):
        if self.running:
            # go through all walkers
            # ask them to perform the A* and work out their route, and to move one square
            nextSet = self.walkers[:]
            for walker in self.walkers:
                result = walker.performAStar(self.gameGrid, self.walkers, self.changed, self.canvas)
                if not result:
                    nextSet.remove(walker)
            self.walkers = nextSet
            self.after(10, self.performAStar)

    def draw(self,e):
        if self.drawing:
            cellx = e.x//30
            celly = e.y//30
            if 0<= cellx <= 19 and 0 <= celly <=  19:  # only if dropped in the grid
                self.gameGrid[celly][cellx] = "X"
                self.canvas.create_rectangle(cellx*30, celly*30, cellx*30+30, celly*30+30, fill="black")

    def startDraw(self,e):
        cellx = e.x//30
        celly = e.y//30
        if 0<= cellx <= 19 and 0 <= celly <=  19:  # only if clicked in the grid
            if self.drawActive:
                self.drawing = True
                self.gameGrid[celly][cellx] = "X"
                self.canvas.create_rectangle(cellx*30, celly*30, cellx*30+30, celly*30+30, fill="black")
            else:
                self.drawing = False
                self.walkers.append(Walker(cellx, celly, self.canvas))

    def erase(self,e):
        cellx = e.x//30
        celly = e.y//30
        if 0<= cellx <= 19 and 0 <= celly <=  19:  
            self.gameGrid[celly][cellx] = None
            self.canvas.create_rectangle(cellx*30, celly*30, cellx*30+30, celly*30+30, fill="lightgreen")

    def stopDraw(self,e):
        self.drawing = False


    def drawGrid(self):
        for row in range(0,599,30):
            for col in range(0,599,30):
                self.canvas.create_rectangle(row,col,row+30, col+30, outline="black")

if __name__ == "__main__":
    app = App()