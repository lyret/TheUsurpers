import pygame, os, sys
from pygame.locals import *

from IdMap import *

"""
class: Screen
A Fullscreen disposable screen
"""
class Screen:
    l = []
    
    def __init__(self, image, disposable=True):
        self.image      = image
        self.disposable = disposable
        Screen.l.append(self)
        
        #Create a unique identity for linking on the gameboard
        self.identity = IdMap.Instance().addLink(self.image, 0, 0, self)
        self.index    = IdMap.Instance().getLastIndex()
        
    def remove(self):
        if self.disposable:
            Screen.l.remove(self)
            IdMap.Instance().removeLink(self.index)