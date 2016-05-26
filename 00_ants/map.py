from tile import Tile
from dirt import Dirt
import pyqtree as qt

class Map:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.map = []
        self.dirtList = []
        for column in range(self.columns):
            self.map.append([])
            for row in range(self.rows):
                self.map[column].append(Tile())
                #self.map[column][row].append(Tile())
                
    def __getitem__(self, index):
        return self.map[index]
        
    def __setitem__(self, index, value):
        self.map[index] = value
                
    def addAnt(self, x, y, ant):
        self.map[int(x)][int(y)].ants.append(ant)
    
    def removeAnt(self, x, y, ant):
        self.map[int(x)][int(y)].ants.remove(ant)
        
    def addDirt(self, dirt):
        self.map[int(dirt.xPos)][int(dirt.yPos)].terrain = dirt
        self.dirtList.append(dirt)
    
    def removeDirt(self, dirt):
        self.map[int(dirt.xPos)][int(dirt.yPos)].terrain = None
        self.dirtList.remove(dirt)
        
    def dirtAt(self, x, y):
        return self.map[int(x)][int(y)].terrain
        
    def addFood(self, x, y, food):
        self.map[int(x)][int(y)].foods.append(food)
        
    def removeFood(self, x, y, food):
        self.map[int(x)][int(y)].foods.remove(food)
        
    def setTerrain(self, x, y, terrain):
        self.map[int(x)][int(y)].terrain = terrain
        
    def dig(self, digTarget, digSpeed, digTime):
            if(digTarget is not None and digTarget in self.dirtList):
                digTarget.amount -= digSpeed * digTime
                if digTarget.amount <= 0:
                    self.dirtList.remove(digTarget)
                    digTarget = None
                return digTarget
            else:
                return None

    def getOccupants(self):
        """ Get all occupants by brute force as a 3-tuple of value, row, and
        col. """
        occs = []
        for row in range(len(self.map)):
            for col in range(len(self.map[0])):
                for entity in self.map[row][col].getOccupants():
                    occs.append((entity, row, col))
        return occs

    def buildQtree(self):
        """ Called inside the rendering loop to construct a quad tree for efficient 
        lookup of nearest neighbors
        """
        self.qtree = qt.Index(bbox=[0,0,600,600])
        for occ, row, col in self.getOccupants():
            self.qtree.insert(item=occ, bbox=[row,col,row,col])

    def findOccupants(self, x, y, r):
        """ Given an (x, y) coordinate and a radius, find all occupants within the
        radius 
        """
        return self.qtree.intersect( (x-r,y-r,x+r,y+r) )



