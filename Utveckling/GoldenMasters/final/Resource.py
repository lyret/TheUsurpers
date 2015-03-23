import pygame, os, sys
from pygame.locals import *

from IdMap        import *
from ResourceType import *



class Resource:

    def __init__(self, name, rType, x, y, province):
            self.name     = name
            self.rType    = getResourceType(rType)
            self.province = province
            self.x        = x
            self.y        = y
            self.identity = IdMap.Instance().addLink(self.rType.image, x, y, self)