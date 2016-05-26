# PyGame Skeleton

import pygame, sys, random
from ant import Ant
from map import Map
from tile import Tile
from food import Food
from dirt import Dirt

GAME_WIDTH = 600
GAME_HEIGHT = 600
antList = []
foodList = []
map = Map(GAME_WIDTH, GAME_HEIGHT)
spawnAnts = False
spawnRAnts = False
spawnBAnts = False
spawnGAnts = False
spawnFood = False
spawnDirt = False
pos = [0,0]

def spawnRedAnts():
    global spawnRedAnts
    global pos
    if(spawnRAnts):
        spawnedRedAnt = Ant()
        spawnedRedAnt.setPos(pos[0], pos[1], map)
        spawnedRedAnt.setFaction("red")
        spawnedRedAnt.setColor()
        antList.append(spawnedRedAnt)

def spawnBlueAnts():
    global spawnBlueAnts
    global pos
    if(spawnBAnts):
        spawnedBlueAnt = Ant()
        spawnedBlueAnt.setPos(pos[0], pos[1], map)
        spawnedBlueAnt.setFaction("blue")
        spawnedBlueAnt.setColor()
        antList.append(spawnedBlueAnt)

def spawnGreenAnts():
    global spawnGreenAnts
    global pos
    if(spawnGAnts):
        spawnedGreenAnt = Ant()
        spawnedGreenAnt.setPos(pos[0], pos[1], map)
        spawnedGreenAnt.setFaction("green")
        spawnedGreenAnt.setColor()
        antList.append(spawnedGreenAnt)

def spawnMouseAnts():
    global spawnAnts
    global pos
    if(spawnAnts):
        spawnedAnt = Ant()
        spawnedAnt.setPos(pos[0], pos[1], map)
        antList.append(spawnedAnt)
        
def spawnMouseFood():
    global spawnFood
    global pos
    if(spawnFood):
        spawnedFood = Food()
        spawnedFood.setPos(pos[0], pos[1], map)
        foodList.append(spawnedFood)
        
def spawnMouseDirt():
    global spawnDirt
    global pos
    if(spawnDirt):
        spawnedDirt = Dirt()
        spawnedDirt.setPos(pos[0], pos[1], map)
        map.dirtList.append(spawnedDirt)
        
def spawn_ants(x):
    redLocation = [random.randint(0, GAME_WIDTH - 1), random.randint(0, GAME_HEIGHT - 1)]
    greenLocation = [random.randint(0, GAME_WIDTH - 1), random.randint(0, GAME_HEIGHT - 1)]
    blueLocation = [random.randint(0, GAME_WIDTH - 1), random.randint(0, GAME_HEIGHT - 1)]

    for number in range(x):
        antList.append(Ant())
        antList[number].setState("wander")
        if(antList[number].faction is "red"):
            antList[number].setPos(redLocation[0], redLocation[1], map)
        if(antList[number].faction is "blue"):
            antList[number].setPos(blueLocation[0], blueLocation[1], map)
        if(antList[number].faction is "green"):
            antList[number].setPos(greenLocation[0], greenLocation[1], map)
            
def spawn_test_ants():
    redLocation = [100, 100]
    greenLocation = [120, 120]
    
    redAnt = Ant()
    redAnt.setFaction("red")
    redAnt.setColor()
    redAnt.health = 25
    redAnt.setPos(redLocation[0], redLocation[1], map)
    antList.append(redAnt)
    
    greenAnt = Ant()
    greenAnt.setFaction("green")
    greenAnt.setColor()
    greenAnt.health = 100
    greenAnt.setPos(greenLocation[0], greenLocation[1], map)
    antList.append(greenAnt)
    
def spawn_test_dirt():
    for column in range(10):
        for row in range(10):
            spawnedDirt = Dirt(row, column, 1)
            map.addDirt(spawnedDirt)
    
def spawn_test_food():
    food = Food()
    food.setPos(300, 300, map)
    foodList.append(food)

def check_events():
    global spawnAnts
    global spawnFood
    global spawnDirt
    global spawnRAnts
    global spawnBAnts
    global spawnGAnts
    global pos
    # loop through all events
    for event in pygame.event.get():
        if(event.type is pygame.QUIT):
            sys.exit()
        elif(event.type is pygame.MOUSEBUTTONDOWN):
            pos = pygame.mouse.get_pos()
            if(event.button is 1):
            # left click spawns ants
                spawnAnts = True
            elif(event.button is 3):
            # right click spawns food
                spawnFood = True
        elif(event.type is pygame.MOUSEBUTTONUP):
        # releasing mouse stops spawning
            spawnAnts = False
            spawnFood = False
        elif(event.type is pygame.KEYDOWN):
            pos = pygame.mouse.get_pos()
            if(event.key is pygame.K_d):
            # pressing d spawns dirt
                spawnDirt = True
            if(event.key is pygame.K_r):
                spawnRAnts = True
            if(event.key is pygame.K_b):
                spawnBAnts = True
            if(event.key is pygame.K_g):
                spawnGAnts = True
        elif(event.type is pygame.KEYUP):
            if(event.key is pygame.K_d):
            # releasing d stops dirt spawning
                spawnDirt = False
            if(event.key is pygame.K_r):
                spawnRAnts = False
            if(event.key is pygame.K_b):
                spawnBAnts = False
            if(event.key is pygame.K_g):
                spawnGAnts = False
            
      
def update_screen():
    screen.fill(pygame.Color('white'))
    
    # draw dirt
    for dirt in map.dirtList:
        pygame.draw.rect(screen, [252, 190, 120], (dirt.xPos, dirt.yPos, 2, 2))
            
    # draw ants
    for ant in antList:
        colorR = ant.getColor()[0]
        colorG = ant.getColor()[1]
        colorB = ant.getColor()[2]
        color = [colorR + random.randint(0, 10), colorG + random.randint(0, 10), colorB + random.randint(0, 10)]
        radius = int(max(2, ant.health/12))
        pygame.draw.circle(screen, color, (int(ant.xPos), int(ant.yPos)), radius)
        
    # draw food
    for food in foodList:
        pygame.draw.rect(screen, food.color, (int(food.xPos - (food.quantity / 4)), int(food.yPos - (food.quantity / 4)), int(food.quantity / 2), int(food.quantity / 2)))
        
    # push the pic
    pygame.display.flip()

def checkDeadAnts():
# stop tracking status of dead ants
    for ant in antList:
        if (ant.health <= 0):
            map.removeAnt(ant.xPos, ant.yPos, ant)
            ant.kill()
            antList.remove(ant)
            
def checkEmptyFood():
# stop tracking the status of finished food
    for food in foodList:
        if(food.quantity <= 0):
            map.removeFood(food.xPos, food.yPos, food)
            food.kill()
            foodList.remove(food)
  
def update_logic(seconds):
    spawnMouseAnts()
    spawnRedAnts()
    spawnBlueAnts()
    spawnGreenAnts()
    spawnMouseFood()
    spawnMouseDirt()
    for ant in antList:
        ant.checkSurroundings(map)
        ant.decide()
        ant.act(map, seconds)
    checkDeadAnts()
    checkEmptyFood()
        

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
    elapsed = clock.tick(60)

# initialise pygame
pygame.init()
screen = pygame.display.set_mode([GAME_WIDTH,GAME_HEIGHT])
screen.fill(pygame.Color('white'))
pygame.display.set_caption("ants")
clock = pygame.time.Clock()
elapsed = 0.
spawn_ants(12)
spawn_test_food()
spawn_test_dirt()

# loop until the user clicks the close button
while True:
    run()
