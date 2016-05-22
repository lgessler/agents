import random

class Dirt:
	def __init__(self, xPos=None, yPos=None, amount=None):
		self.amount = amount if amount else random.randint(1, 3)
		self.xPos = xPos if xPos is not None else None
		self.yPos = yPos if yPos is not None else None
		
	def setPos(self, xPos, yPos, map):
		self.xPos = xPos
		self.yPos = yPos
		map.addDirt(self)