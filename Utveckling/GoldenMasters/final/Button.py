import pygame, os, sys
from pygame.locals import *

from IdMap import *

"""
class: Button
A Clickable button
"""
class Button:

    def __init__(self, (x, y, width, height), text, function, args, (color1, bg1), (color2, bg2)):
        self.text        = text
        self.color    = [color1, color2]
        self.bgColor     = [bg1, bg2]
        self.x           = x
        self.y           = y
        self.width       = width
        self.height      = height
        self.image       = pygame.Surface((width, height))
        self.image.fill((255,255,255))
        
        self.function    = function
        self.args        = args
        self.active      = False
        
        #Create a unique identity for linking on the gameboard
        self.identity = IdMap.Instance().addLink(self.image, self.x, self.y, self)
        self.index    = IdMap.Instance().getLastIndex()
        IdMap.Instance().setStatus(self.index, False)
        
    
    def setStatus(self, status):
        self.active = status
        
        IdMap.Instance().setStatus(self.index, status)