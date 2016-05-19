import itertools, random
from map import Map

factionList = ["red", "blue", "green"]
stateList = ["attack", "attackMove", "wander"]

#this controls the length/width of the square used by each ant to check for enemies and friends around it
checkRadius = 25

GAME_WIDTH = 600
GAME_HEIGHT = 600

class Ant:
	def __init__(self, xPos=None, yPos=None, health=None, dmg=None, speed=None, faction=None, color=None):
		self.xPos = xPos
		self.yPos = yPos
		self.health = health
		self.dmg = dmg
		self.speed = speed
		self.faction = faction
		self.color = color
		self.friendlySurroundings = []
		self.hostileSurroundings = []
		self.state = "wander"
		self.antToAttack = None
		if(self.xPos is None):
			self.xPos = random.randint(0, GAME_WIDTH - 1)
		if(self.yPos is None):
			self.yPos = random.randint(0, GAME_HEIGHT - 1)
		if(self.health is None):
			self.health = random.uniform(5, 40)
		if(self.speed is None):
			self.speed = random.uniform(10, 25)
		if(self.dmg is None):
			self.dmg = random.uniform(100, 125)
		if(self.faction is None):
			self.faction = factionList[random.randint(0, 2)]
		if(self.color is None):
			self.setColor()
			
	def kill(self):
		self.xPos = 1000
		self.yPos = 1000
		self.health = 0
		self.dmg = 0
		self.speed = 0
		self.faction = None
		self.color = None
		self.friendlySurroundings = []
		self.hostileSurroundings = []
		self.state = None
		self.antToAttack = None
			
	def setColor(self):
		if(self.faction == "red"):
			self.color = [random.randint(0, 75) + 170, 0, 0]
		if(self.faction == "green"):
			self.color = [0, random.randint(0, 75) + 170, 0]
		if(self.faction == "blue"):
			self.color = [0, 0, random.randint(0, 75) + 170]
			
	def getColor(self):
		return self.color
		
	def setFaction(self, faction):
		self.faction = faction
		
	def setState(self, state):
		self.state = state
  
	def setPos(self, x, y, map):
		self.xPos = x
		self.yPos = y
		map[int(self.xPos)][int(self.yPos)].append(self)
      
	def move(self, x, y, map, seconds):
		map[int(self.xPos)][int(self.yPos)].remove(self)
		self.xPos += x * self.speed * seconds
		if(self.xPos < 0):
			self.xPos = 0
		if(self.xPos > (GAME_WIDTH - 1)):
			self.xPos = GAME_WIDTH - 1
		self.yPos += y * self.speed * seconds
		if(self.yPos < 0):
			self.yPos = 0
		if(self.yPos > GAME_HEIGHT - 1):
			self.yPos = GAME_HEIGHT - 1
		map[int(self.xPos)][int(self.yPos)].append(self)
		
	def getSign(self, x):
		if (x > 0):
			return 1
		if (x < 0):
			return -1
		return 0
		
	def attackMove(self, map, seconds):
		map[int(self.xPos)][int(self.yPos)].remove(self)
		
		#handle new X coordinate position
		originalXSign = self.getSign(self.antToAttack.xPos - self.xPos)
		self.xPos += self.getSign(self.antToAttack.xPos - self.xPos) * self.speed * seconds
		newXSign = self.getSign(self.antToAttack.xPos - self.xPos)
		if (originalXSign != newXSign):
			# this means the ant has moved too far in the direction of its target, so
			# instead we should just set its position to its target's position
			self.xPos = self.antToAttack.xPos
		if(self.xPos < 0):
			self.xPos = 0
		if(self.xPos > (GAME_WIDTH - 1)):
			self.xPos = GAME_WIDTH - 1
		
		#handle new Y coordinate position
		originalYSign = self.getSign(self.antToAttack.yPos - self.yPos)
		self.yPos += self.getSign(self.antToAttack.yPos - self.yPos) * self.speed * seconds
		newYSign = self.getSign(self.antToAttack.yPos - self.yPos)
		if (originalYSign != newYSign):
			# this means the ant has moved too far in the direction of its target, so
			# instead we should just set its position to its target's position
			self.yPos = self.antToAttack.yPos
		if(self.yPos < 0):
			self.yPos = 0
		if(self.yPos > (GAME_HEIGHT - 1)):
			self.yPos = GAME_HEIGHT - 1
			
		map[int(self.xPos)][int(self.yPos)].append(self)

	def checkSurroundings(self, map):
		#update hostilesurroundings and friendlysurroundings based on nearby ants on the map
		self.friendlySurroundings[:] = []
		self.hostileSurroundings[:] = []
		minCheckX = max(0, int(self.xPos) - checkRadius)
		maxCheckX = min(GAME_WIDTH - 1, int(self.xPos) + checkRadius)
		minCheckY = max(0, int(self.yPos) - checkRadius)
		maxCheckY = min(GAME_HEIGHT - 1, int(self.yPos) + checkRadius)

		for row in range(minCheckX, maxCheckX):
			for column in range(minCheckY, maxCheckY):
				if(len(map[row][column]) != 0):
					for ant in map[row][column]:
						if(ant.faction is self.faction):
							if(len(self.friendlySurroundings) > 5):
							#ants, having poor memories, can only recognize up to 5 nearby comrades
								break
							self.friendlySurroundings.append(ant)
						else:
							if(len(self.hostileSurroundings) > 5):
							#ants, having poor memories, can only recognize up to 5 nearby enemies
								break
							self.hostileSurroundings.append(ant)

		if(len(self.hostileSurroundings) is 0):
			self.state = "wander"
		elif(len(self.hostileSurroundings) is not 0):
			if self.antToAttack not in self.hostileSurroundings:
				#if the ant we were attacking has left our hostileSurroundings, find a new ant to attack
				self.antToAttack = self.hostileSurroundings[random.randint(0, (len(self.hostileSurroundings) - 1))]
			if(abs(self.xPos - self.antToAttack.xPos) <= 6) and (abs(self.yPos - self.antToAttack.yPos) <= 6):
				#ant in range
				self.state = "attack"
			else:
				self.state = "attackMove"
		else:
			self.state = "wander"
			

	def act(self, map, seconds):
		if(self.state is "attack"):
			self.antToAttack.health -= self.dmg * seconds
			if(self.antToAttack.health <= 0):
				self.health += self.antToAttack.health / 2
				self.hostileSurroundings.remove(self.antToAttack)
				self.antToAttack = None
		if(self.state is "attackMove"):
			self.attackMove(map, seconds)
		if(self.state is "wander"):
			self.move(random.randint(-1, 1), random.randint(-1, 1), map, seconds)
    
    
'''what if the color is randomly assigned and the closer an ant is to another ant's color, the friendlier they are '''
    