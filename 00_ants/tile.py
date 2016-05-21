from dirt import Dirt

class Tile:
	def __init__(self, terrain=None, ants=None, foods=None):
		self.terrain = None
		self.ants = ants
		self.foods = foods
		if(self.ants is None):
			self.ants = []
		if(self.foods is None):
			self.foods = []
			
	def getOccupants(self):
		fullList = self.ants + self.foods
		return fullList