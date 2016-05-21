from tile import Tile
from dirt import Dirt

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
		
	def addFood(self, x, y, food):
		self.map[int(x)][int(y)].foods.append(food)
		
	def removeFood(self, x, y, food):
		self.map[int(x)][int(y)].foods.remove(food)
		
	def setTerrain(self, x, y, terrain):
		self.map[int(x)][int(y)].terrain = terrain
		
	def dig(self, digTarget, digSpeed, digTime):
			digTarget.amount -= digSpeed * digTime
			if digTarget.amount <= 0:
				self.digList.remove(digTarget)
				digTarget = None
			return digTarget