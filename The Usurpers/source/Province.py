import pygame, os, sys
from pygame.locals import *

from IdMap    import *
from Resource import *
from Player   import *
from Unit     import *
from Army     import *



"""
Returns the instance of a province type with a specified number (string).
"""
def getProvince(string):
    return Province.dictionary[string]


    
"""
Class: Province
Represents a province (an area, land or country in risk).
"""
class Province:
    dictionary = {}
                           
    def __init__(self, ident, x, y):
        self.ident      = str(ident)
        self.neighbours = {}
        self.image      = pygame.image.load(os.path.join('data', 'provinces', self.ident, 'img.png'))
        self.x          = x
        self.y          = y
        
        #Add the province to the dictionary.
        Province.dictionary[self.ident] = self
        
        #Add to id-map
        self.identity = IdMap.Instance().addLink(self.image, x, y, self)
        
        #Load informations from the data folder.
        with open(os.path.join('data', 'provinces', self.ident, 'information.txt'), 'r') as f:
            
            #Temporary
            self.adjacent = f.readline().split()
            army = []
            
            #Name
            self.name = f.readline().decode('utf8').strip('\n')

            #Controlling faction and starting army
            d = f.readline().decode('utf8').strip('\n')
            if(len(d) != 0):
                d = d.split()
                self.controller =  Player(d[0], True)
                d.pop(0)
                army = []
                for ut in d:
                    army.append(Unit(getUnitType(ut)))
            else:
                self.controller = None
            
            #Resource
            d = f.readline().decode('utf8').strip('\n')
            if(len(d) != 0):
                d = d.split()
                self.resource = Resource(f.readline().decode('utf8').strip('\n'), d[0], int(d[1]), self.y + int(d[2]), self)
            else:
                self.resource = None
                f.readline()
                
            #Army and flag position
            d = f.readline().split()
            self.flagX = int(d[0])
            self.flagY = int(d[1]) + self.y
            
            if len(army) > 0:
                self.army = Army(self.flagX, self.flagY, self, army)
            else:
                self.army = None
                
            #Description
            self.description = ""
            for l in f.readlines():
                self.description += l.decode('utf8')
            f.close()

        #Adjust images
        self.image = self.image.convert()
        self.image.set_colorkey((0,0,0))


    #Method: setAlpha - Sets the opacity the province is drawn at
    def setAlpha(self, alpha):
        self.image.set_alpha(alpha)
        
    def addArmy(self, army):
        self.army = army
        army.province = self
        army.x = self.flagX
        army.y = self.flagY