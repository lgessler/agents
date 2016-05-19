# PyGame Skeleton

import pygame, sys, random
from ant import Ant
from map import Map

GAME_WIDTH = 600
GAME_HEIGHT = 600
antList = []
deadAnts = []
map = Map(GAME_WIDTH, GAME_HEIGHT)
spawnAnts = False
pos = [0,0]

def spawnMouseAnts():
	global spawnAnts
	global pos
	if(spawnAnts):
		spawnedAnt = Ant()
		spawnedAnt.setPos(pos[0], pos[1], map.map)
		antList.append(spawnedAnt)

def spawn_ants(x):
	redLocation = [random.randint(0, GAME_WIDTH - 1), random.randint(0, GAME_HEIGHT - 1)]
	greenLocation = [random.randint(0, GAME_WIDTH - 1), random.randint(0, GAME_HEIGHT - 1)]
	blueLocation = [random.randint(0, GAME_WIDTH - 1), random.randint(0, GAME_HEIGHT - 1)]

	for number in range(x):
		antList.append(Ant())
		antList[number].setState("wander")
		if(antList[number].faction is "red"):
			antList[number].setPos(redLocation[0], redLocation[1], map.map)
		if(antList[number].faction is "blue"):
			antList[number].setPos(blueLocation[0], blueLocation[1], map.map)
		if(antList[number].faction is "green"):
			antList[number].setPos(greenLocation[0], greenLocation[1], map.map)
			
def spawn_test_ants():
	redLocation = [100, 100]
	greenLocation = [120, 120]
	
	redAnt = Ant()
	redAnt.setFaction("red")
	redAnt.setColor()
	redAnt.health = 25
	redAnt.setPos(redLocation[0], redLocation[1], map.map)
	antList.append(redAnt)
	
	greenAnt = Ant()
	greenAnt.setFaction("green")
	greenAnt.setColor()
	greenAnt.health = 100
	greenAnt.setPos(greenLocation[0], greenLocation[1], map.map)
	antList.append(greenAnt)

def check_events():
	global spawnAnts
	global pos
	# loop through all events
	for event in pygame.event.get():
		if(event.type is pygame.QUIT):
			sys.quit()
		if(event.type is pygame.MOUSEBUTTONDOWN):
			print("mdown")
			spawnAnts = True
			pos = pygame.mouse.get_pos()
		if(event.type is pygame.MOUSEBUTTONUP):
			print("mup")
			spawnAnts = False
      
def update_screen():
	screen.fill(pygame.Color('white'))
	for ant in antList:
		colorR = ant.getColor()[0]
		colorG = ant.getColor()[1]
		colorB = ant.getColor()[2]
		color = [colorR + random.randint(0, 10), colorG + random.randint(0, 10), colorB + random.randint(0, 10)]
		radius = int(max(1, ant.health/7))
		pygame.draw.circle(screen, color, (int(ant.xPos), int(ant.yPos)), radius)
	pygame.display.flip()

def checkDeadAnts():
	for ant in antList:
		if (ant.health <= 0):
			ant.kill()
			antList.remove(ant)
  
def update_logic(seconds):
	spawnMouseAnts()
	for ant in antList:
		'''
		print("---")
		print("Ant health: " + str(ant.health))
		print("Ant state: " + ant.state)
		print("Ant hostile list: " + str(ant.hostileSurroundings))
		print("---")
		'''
		ant.checkSurroundings(map.map)
		ant.act(map.map, seconds)
	checkDeadAnts()
		

def run():
	global pos
	global elapsed
	pos = pygame.mouse.get_pos()
	
	#update clock info
	seconds = elapsed/1000.0
	
  # check events
	check_events()
  
	# update logic of game based on time elapsed, to standardize computation
	update_logic(seconds)

	# update the screen with what we've drawn
	update_screen()

	# control the draw update speed
	elapsed = clock.tick(50)

# initialise pygame
pygame.init()
screen = pygame.display.set_mode([GAME_WIDTH,GAME_HEIGHT])
screen.fill(pygame.Color('white'))
pygame.display.set_caption("ants")
clock = pygame.time.Clock()
elapsed = 0.
spawn_ants(333)

# loop until the user clicks the close button
while True:
	run()