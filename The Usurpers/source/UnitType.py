import pygame, os, sys
from pygame.locals import *



"""
Returns the instance of a unit type with a specified name, if it exists. 
if it does not exists is is created.
"""
def getUnitType(string):
    try:
        return UnitType.dictionary[string]
    except:
        return UnitType(string)
            
            
            
"""
Class: Unit Type
Represents a type of unit and its standard values.
"""
class UnitType:
    dictionary = {}

    def __init__(self, name): 
        self.name          = name
        self.strongAgainst = []
        self.image         = pygame.image.load(os.path.join('data', 'units', name, 'img.png'))
        
        #Add the type to the dictionary.
        UnitType.dictionary[name] = self
        
        #Load informations from the data folder.
        with open(os.path.join('data', 'units', name,  'information.txt'), 'r') as f:
            
            #Units this type is strong against
            d = f.readline().split()
            for line in d:
                self.strongAgainst.append(getUnitType(line))
            
            #Description
            self.description = ""
            for l in f.readlines():
                self.description += l.decode('utf8')
            f.close()