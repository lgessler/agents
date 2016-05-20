import itertools, random
from map import Map

GAME_WIDTH = 600
GAME_HEIGHT = 600

class Food:
	def __init__(self, xPos = None, yPos = None, quantity = None, quality = None):
		self.type = "food"
		self.xPos = xPos
		self.yPos = yPos
		self.quantity = quantity
		self.quality = quality
		if(self.xPos is None):
			self.xPos = random.randint(0, GAME_WIDTH - 1)
		if(self.yPos is None):
			self.yPos = random.randint(0, GAME_HEIGHT - 1)
		if(self.quantity is None):
			self.quantity = random.randint(1, 25)
		if(self.quality is None):
			self.quality = random.randint(1, 10)
			self.quality = max(1, self.quality - 5)
		
	def setPos(self, xPos, yPos, map):
		self.xPos = xPos
		self.yPos = yPos
		map[int(self.xPos)][int(self.yPos)].append(self)
		