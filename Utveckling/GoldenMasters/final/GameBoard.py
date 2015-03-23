import pygame, os, sys
from pygame.locals import *

from Singleton import *
from Province  import *



"""
Class: Gameboard
Represents a the map of provinces. (singleton)
"""
@Singleton
class GameBoard:
    
    def __init__(self):
        self.mapImage     = pygame.image.load(os.path.join('data', 'common', 'gameboard', 'img.png'))
        self.bordersImage = pygame.image.load(os.path.join('data', 'common', 'borders' , 'img.png'))
        self.provinces    = []
        self.resources    = []
        self.armies       = []
        self.players      = []
        
        #Load informations from the data folder.
        with open(os.path.join('data', 'game', 'information.txt'), 'r') as f:
            lines = f.readlines()
            
            #Size and position
            self.width   = int(lines[4].decode('utf8').strip('\n'))
            self.height  = int(lines[5].decode('utf8').strip('\n'))
            self.yOffset = int(lines[6].decode('utf8').strip('\n'))/2
            
            #Mapsize
            self.mapSize = int(lines[12].decode('utf8').strip('\n'))
            f.close()
                
        #Load provinces.
        for i in range(1, self.mapSize+1):
            p = Province(i, 0, self.yOffset)
            
            self.provinces.append(p)
            if p.resource != None:
                self.resources.append(p.resource)
            if p.army != None:
                self.armies.append(p.army)
            if p.controller != None:
                self.players.append(p.controller)
            
        #Finialize the map by joining all neighbors correctly and
        #adding them to the id-map
        for k, p in Province.dictionary.iteritems():
            for a in p.adjacent:
                n = getProvince(a)
                p.neighbours[a] = n
                n.neighbours[str(p.ident)] = p