import random

class Dirt:
	def __init__(self, xPos=None, yPos=None, amount=None):
		self.amount = amount if amount else random.randint(1, 3)
		self.xPos = xPos if xPos else None
		self.yPos = yPos if yPos else None
		