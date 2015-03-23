import pygame, os, sys
from pygame.locals import *

from IdMap import *


"""
Class: Army
An army positioned on a province. represented by a flag on the board.
"""
class Army:
	shadowImage = pygame.image.load(os.path.join('data', 'common', 'shadows', 'flag.png'))
	flagImage	= {'blue':[], 'red':[], 'white':[], 'gold':[]}
	
	for i in range(6):
		flagImage['blue'].append(pygame.image.load(os.path.join('data', 'flags', 'blue', str(i)+'.png')))
		flagImage['red'].append(pygame.image.load(os.path.join('data', 'flags', 'red', str(i)+'.png')))
		flagImage['white'].append(pygame.image.load(os.path.join('data', 'flags', 'white', str(i)+'.png')))
		flagImage['gold'].append(pygame.image.load(os.path.join('data', 'flags', 'gold', str(i)+'.png')))
	
	
	
	def __init__(self, x, y, province, units = []):
		self.shadow	= Army.shadowImage
		self.province = province
		self.units	= units
		self.number	= len(self.units)
		self.image	= Army.flagImage[self.province.controller.color][self.number]
		self.x		= x
		self.y		= y
		self.identity = IdMap.Instance().addLink(self.image, self.x, self.y, self.province, self.province.identity)

	#updates the image to match the units in the army and removes dead units
	def update(self):
		self.units = [x for x in self.units if x.health>0]
		self.number = len(self.units)

		self.image = Army.flagImage[self.province.controller.color][self.number]