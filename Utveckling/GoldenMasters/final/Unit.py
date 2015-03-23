import pygame, os, sys
from pygame.locals import *

from UnitType import *



"""
Class: Unit
A individual unit of a specific typ.
"""
class Unit:

    def __init__(self, unitType):
		self.uType  = unitType
		self.health = 100