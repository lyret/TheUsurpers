import pygame, os, sys
from pygame.locals import *

from Singleton import *



"""
Class: IdMap
the idMap represents a map the size of the window that contains all clickable object
drawn in a specific color-key. By getting the color-value of the surface at a position it
can be determined if a object should be activated, this allows for pixel based detection of mouse events instead
of using pygame's rectangle based method.
"""
@Singleton
class IdMap:

    def __init__(self):
        
        self.links    = []
        self.buffert  = 4
        self.reserved = 5
        self.total    = self.buffert+self.reserved 
        
        #Load informations from the data folder.
        with open(os.path.join('data', 'game', 'information.txt'), 'r') as f:
            lines = f.readlines()
            
            #Size and position
            width   = int(lines[4].decode('utf8').strip('\n'))
            height  = int(lines[5].decode('utf8').strip('\n'))
            height += int(lines[6].decode('utf8').strip('\n'))
            f.close()
            
        #Create the surface for storing links
        self.image = pygame.Surface((width, height))
        

    #Adds a object to the id map (surface, x, y, object), optionally lets yo specify the
    #color value for linking several areas of the screen to one object. returns the identity of the added object
    def addLink(self, targetSurface, x, y, targetObject, identity = 0):
        
        if identity == 0:
            self.total += self.buffert
            identity = self.total
    
        pixels = pygame.PixelArray(targetSurface)
        pixels = pixels.extract(0, 0.1)
        pixels.replace(0, (identity, 0, 255), 0.1)
        pixels.replace((255,255,255), 0, 0.1)
        targetSurface = pixels.make_surface()
        
        self.links.append([targetSurface, x, y, targetObject, identity, True])
        
        return identity
        
        
    #Returns the object that exists at a position
    def get(self, (x, y)):
        pos = (x, y)
        
        if not self.image.get_rect().collidepoint(pos):
            return None
        
        value = self.image.get_at(pos)
        value = value[0]
        
        if value == (0,255,0):
            return None
        
        for l in self.links:
            if l[4] == value:
                return l[3]   
        return None

    #Updates the id map
    def update(self):
        self.image.fill((0, 255, 0))
        
        for l in self.links:
            if l[5]:
                self.image.blit(l[0], (l[1], l[2]))

  
    #Returns the latest index of the link list
    def getLastIndex(self):
        return (len(self.links)-1)

    #Removes a link at the given index
    def removeLink(self, index):
        self.links.pop(index)
        
    #Sets the status of a link at the given index
    def setStatus(self, index, status):
        self.links[index][5] = status