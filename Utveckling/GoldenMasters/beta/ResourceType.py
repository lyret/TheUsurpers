import pygame, os, sys
from pygame.locals import *

from UnitType import *



"""
Returns the instance of a resource type with a specified name, if it exists. 
if it does not exists is is created.
"""
def getResourceType(string):
    try:
        return ResourceType.dictionary[string]
    except:
        return ResourceType(string)
            
            
            
"""
Class: Resource Type
Represents a type of resource and its standard values.
"""
class ResourceType:
    dictionary = {}
    shadowImage = pygame.image.load(os.path.join('data', 'common', 'shadows', 'resource.png'))

    def __init__(self, name):
        self.name   = name
        self.image  = pygame.image.load(os.path.join('data', 'resources', name, 'img.png'))
        self.shadow = ResourceType.shadowImage
        
        #Add the type to the dictionary.
        ResourceType.dictionary[name] = self
        
        #Load informations from the data folder.
        with open(os.path.join('data', 'resources', name,  'information.txt'), 'r') as f:
            
            #Allows for the production of this unit
            self.canProduce = getUnitType(f.readline().decode('utf8').strip('\n'))
            
            #Description
            self.description = ""
            for l in f.readlines():
                self.description += l.decode('utf8')
            f.close()