class Tile:
	def __init__(self, terrain=None, ants=None, foods=None):
		self.terrain = terrain
		self.ants = ants
		self.foods = foods
		if(self.terrain is None):
			self.terrain = "dirt"
		if(self.ants is None):
			self.ants = []
		if(self.foods is None):
			self.foods = []
			
	def getOccupants(self):
		fullList = self.ants + self.foods
		return fullList