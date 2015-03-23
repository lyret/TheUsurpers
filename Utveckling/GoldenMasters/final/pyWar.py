import pygame, os, sys, random
from pygame.locals import *

from GameManager import *

"""
MAIN (INITIALIZATION)
"""
def main():

    #Init pygame.
    pygame.init()
    pygame.display.set_mode((1200, 700))
    
    #Create a new game.
    manager = GameManager.Instance()
    
    #Start looping.
    while True:
        manager.loop()
    
    

#Only run the game when executed directly.
if __name__ == "__main__":
    main()