import itertools, random
from map import Map

GAME_WIDTH = 600
GAME_HEIGHT = 600

class AntSquad:
    def __init__(self, ants, leader):
        ants = ants
        leader = leader
        
    def add(self, ant):
        if(ant not in self.ants):
            self.ants.append(ant)
            
    def remove(self, ant):
        if(ant in self.ants):
            self.ants.remove(ant)
            
    def setLeader(self, leader):
        if(leader not in self.ants):
            self.ants.append(leader)
        self.leader = leader
        
    def move(self, x, y, map):
        self.leader.move(x, y, map)
        for ant in self.ants:
            if (ant is not self.leader):
                ant.followTheLeader()
