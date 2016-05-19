class Map:
	def __init__(self, rows, columns):
		self.rows = rows
		self.columns = columns
		self.map = []
		for column in range(self.columns):
			self.map.append([])
			for row in range(self.rows):
				self.map[column].append([])