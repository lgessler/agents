import itertools, random, math
from map import Map

factionList = ["red", "blue", "green"]
stateList = ["attack", "attackMove", "wander"]

#this controls the length/width of the square used by each ant to check for enemies and friends around it
enemyCheckRadius = 50

#this controls the length/width of the square used by each ant to check for enemies and friends around it
foodCheckRadius = 150

GAME_WIDTH = 600
GAME_HEIGHT = 600

class Ant:
	def __init__(self, xPos=None, yPos=None, health=None, dmg=None, speed=None, faction=None, color=None):
		self.type = "ant"
		self.xPos = xPos
		self.yPos = yPos
		self.health = health
		self.dmg = dmg
		self.speed = speed
		self.faction = faction
		self.color = color
		self.friendlySurroundings = []
		self.hostileSurroundings = []
		self.foodSurroundings = []
		self.state = "wander"
		self.antToAttack = None
		self.squad = None
		self.foodSource = None
		if(self.xPos is None):
			self.xPos = random.randint(0, GAME_WIDTH - 1)
		if(self.yPos is None):
			self.yPos = random.randint(0, GAME_HEIGHT - 1)
		if(self.health is None):
			self.health = random.uniform(5, 40)
		if(self.speed is None):
			self.speed = random.uniform(20, 35)
		if(self.dmg is None):
			self.dmg = random.uniform(2, 6)
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
		
	def distanceTo(self, entity):
		if(entity is None):
			return 99999
		xDistance = abs(self.xPos - entity.xPos)
		yDistance = abs(self.yPos - entity.yPos)
		return xDistance + yDistance
			
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
		
	def joinSquad(self, squad):
		squad.add(self)
		
	def normalize(self, v):
		lengthSquared = v[0] * v[0] + v[1] * v[1];
		if (lengthSquared is not 0):
			length = math.sqrt(lengthSquared)
			v[0] /= length
			v[1] /= length
		return v
      
	def move(self, x, y, map, seconds):
		map[int(self.xPos)][int(self.yPos)].remove(self)
		moveVect = self.normalize([x, y])
		x = moveVect[0]
		y = moveVect[1]
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
		
	def attack(self, target, seconds):
		target.health -= self.dmg * seconds
		if(target.health <= 0):
				self.health += target.health / 2
				self.dmg += 1
				self.hostileSurroundings.remove(target)
				self.antToAttack = None
		
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
		
	def eat(self, seconds):
		if(self.foodSource.quantity <= 0):
			self.foodSurroundings.remove(self.foodSource)
			self.foodSource = None
		else:
			plusMod = self.foodSource.quality
			foodEaten = seconds
			self.foodSource.quantity -= seconds
			self.health += seconds * plusMod
			self.dmg += seconds * plusMod * .2

	def eatMove(self, map, seconds):
		map[int(self.xPos)][int(self.yPos)].remove(self)
		
		#handle new X coordinate position
		originalXSign = self.getSign(self.foodSource.xPos - self.xPos)
		self.xPos += self.getSign(self.foodSource.xPos - self.xPos) * self.speed * seconds
		newXSign = self.getSign(self.foodSource.xPos - self.xPos)
		if (originalXSign != newXSign):
			# this means the ant has moved too far in the direction of its target, so
			# instead we should just set its position to its target's position
			self.xPos = self.foodSource.xPos
		if(self.xPos < 0):
			self.xPos = 0
		if(self.xPos > (GAME_WIDTH - 1)):
			self.xPos = GAME_WIDTH - 1
		
		#handle new Y coordinate position
		originalYSign = self.getSign(self.foodSource.yPos - self.yPos)
		self.yPos += self.getSign(self.foodSource.yPos - self.yPos) * self.speed * seconds
		newYSign = self.getSign(self.foodSource.yPos - self.yPos)
		if (originalYSign != newYSign):
			# this means the ant has moved too far in the direction of its target, so
			# instead we should just set its position to its target's position
			self.yPos = self.foodSource.yPos
		if(self.yPos < 0):
			self.yPos = 0
		if(self.yPos > (GAME_HEIGHT - 1)):
			self.yPos = GAME_HEIGHT - 1
			
		map[int(self.xPos)][int(self.yPos)].append(self)
		
	def flee(self, map, seconds):
		#map[int(self.xPos)][int(self.yPos)].remove(self)
		xTotal = 0
		yTotal = 0
		for enemy in self.hostileSurroundings:
			xTotal += enemy.xPos
			yTotal += enemy.yPos
		xAvg = xTotal / len(self.hostileSurroundings)
		yAvg = yTotal / len(self.hostileSurroundings)
		xMoveDir = self.getSign(self.xPos - xAvg)
		yMoveDir = self.getSign(self.yPos - xAvg)
		
		self.move(xMoveDir, yMoveDir, map, seconds)
		'''
		xMoveDir = self.getSign(self.xPos - xAvg)
		self.xPos += xMoveDir * self.speed * seconds
		if(self.xPos < 0):
			self.xPos = 0
		if(self.xPos > (GAME_WIDTH - 1)):
			self.xPos = GAME_WIDTH - 1
		
		yMoveDir = self.getSign(self.yPos - xAvg)
		self.yPos += yMoveDir * self.speed * seconds
		if(self.yPos < 0):
			self.yPos = 0
		if(self.yPos > (GAME_HEIGHT - 1)):
			self.yPos = GAME_HEIGHT - 1
		'''
		#map[int(self.xPos)][int(self.yPos)].append(self)

	def checkSurroundings(self, map):
		#update hostilesurroundings and friendlysurroundings based on nearby ants on the map
		self.friendlySurroundings[:] = []
		self.hostileSurroundings[:] = []
		self.foodSurroundings[:] = []
		minCheckX = max(0, int(self.xPos) - enemyCheckRadius)
		maxCheckX = min(GAME_WIDTH - 1, int(self.xPos) + enemyCheckRadius)
		minCheckY = max(0, int(self.yPos) - enemyCheckRadius)
		maxCheckY = min(GAME_HEIGHT - 1, int(self.yPos) + enemyCheckRadius)

		for row in range(minCheckX, maxCheckX):
			for column in range(minCheckY, maxCheckY):
				if(len(map[row][column]) != 0):
					for entity in map[row][column]:
						if(entity.type is "ant"):
							if(entity.faction is self.faction):
								if(len(self.friendlySurroundings) > 50):
								#ants, having poor memories, can only recognize up to 5 nearby comrades
									break
								self.friendlySurroundings.append(entity)
							else:
								if(len(self.hostileSurroundings) > 50):
								#ants, having poor memories, can only recognize up to 5 nearby enemies
									break
								self.hostileSurroundings.append(entity)
								
						if(entity.type is "food"):
							if(len(self.foodSurroundings) > 5):
								break
							self.foodSurroundings.append(entity)
			
	def decide(self):

		if(len(self.hostileSurroundings) is not 0):
		#first priority is enemy ants in the vicinity
			if(self.health < 5):
			#low hp = flee
				self.state = "flee"
			if(len(self.hostileSurroundings) <= len(self.friendlySurroundings) + 1):
			#engage if it's at least a roughly proportional fight
				if self.antToAttack not in self.hostileSurroundings:
					#if the ant we were attacking has left our hostileSurroundings, find a new ant to attack
					self.antToAttack = self.hostileSurroundings[random.randint(0, (len(self.hostileSurroundings) - 1))]
				#if(abs(self.xPos - self.antToAttack.xPos) <= 6) and (abs(self.yPos - self.antToAttack.yPos) <= 6):
				if(self.distanceTo(self.antToAttack) <= 5):
					#ant in range
					self.state = "attack"
					return "attack"
				else:
					self.state = "attackMove"
					return "attackMove"
			else:
				self.state = "flee"
		elif(len(self.foodSurroundings) is not 0):
		#if the coast is clear, deal with nearby food
			foodSourceDistance = self.distanceTo(self.foodSource)
			for foodsource in self.foodSurroundings:
				curFoodSourceDistance = self.distanceTo(foodsource)
				if(curFoodSourceDistance < foodSourceDistance):
					foodSourceDistance = curFoodSourceDistance
					self.foodSource = foodsource
			if(self.distanceTo(self.foodSource) <= 5):
				self.state = "eat"
				return "eat"
			else:
				self.state = "eatMove"
				return "eatMove"
		else:
			self.state = "wander"
			return "wander"
			

	def act(self, map, seconds):
		if(self.state is "attack"):
			self.attack(self.antToAttack, seconds)
		elif(self.state is "attackMove"):
			self.attackMove(map, seconds)
		elif(self.state is "eat"):
			self.eat(seconds)
		elif(self.state is "eatMove"):
			self.eatMove(map, seconds)
		elif(self.state is "flee"):
			self.flee(map, seconds)
		elif(self.state is "wander"):
			self.move(random.randint(-1, 1), random.randint(-1, 1), map, seconds)
    
    
'''what if the color is randomly assigned and the closer an ant is to another ant's color, the friendlier they are '''
    