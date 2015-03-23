import pygame, os, sys
from pygame.locals import *



"""
Returns the instance of a player with a specified number (string).
"""
def getPlayer(string):
	return Player.dictionary[string]
	
	
	
"""
Class: Player
A AI or Human controlled player.
"""
class Player:
	dictionary = {}
	
	def __init__(self, ident, human):
		self.ident    = str(ident)
		self.human    = human
		
		#Add the player to the dictionary.
		Player.dictionary[self.ident] = self
				
		#Load informations from the data folder.
		with open(os.path.join('data', 'players', self.ident, 'information.txt'), 'r') as f:
			
			#Name
			self.name = f.readline().decode('utf8').strip('\n')
			
			#Starting money
			self.cash  =  int(f.readline().decode('utf8').strip('\n'))
					
			#Faction colors
			self.color      = f.readline().decode('utf8').strip('\n')
			d = f.readline().decode('utf8').strip('\n').split(',') 
			self.colorValue = (int(d[0]), int(d[1]), int(d[2]))
			
			#Description
			self.description = ""
			for l in f.readlines():
				self.description += l.decode('utf8')
			f.close()