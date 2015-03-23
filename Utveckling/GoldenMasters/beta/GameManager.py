import pygame, os, sys, random
from pygame.locals import *

from Singleton     import *
from GameBoard     import *
from GameInterface import *
from IdMap         import *

#TEMP
from Button   import *
from Army     import *
from Unit     import *
from UnitType import *

"""
Class: Game Manager
A singelton class (allows for a global, single, instance of the class) that keeps
track of the game state and available actions.
"""
@Singleton
class GameManager:

    def __init__(self):
        self.framerate     = 60
        self.mousePosition = (0, 0)
        self.timer         = pygame.time.Clock()
                
        #Keep track of turns.
        self.currentPlayer = None
        self.currentTurn   = 0
        self.latestSelection = {}
        
        self.attackMove = 1
        self.buyMove    = 1
        
        #Keep track of selection.
        self.hovered  = None
        self.selected = None
        self.previous = None
        
        #Create interface and map logic.
        self.idMap         = IdMap.Instance()
        self.board         = GameBoard.Instance()
        self.interface     = GameInterface.Instance()
        self.interface.manager = self
        
        #Control panel TEMP
        self.attackButton  = Button((878, 535, 124, 30), "Attack", self.attack, None,
                                        ((240, 255, 180), (160, 172, 110)),
                                        ((0, 0, 0), (160, 172, 110)))
        self.buyButton     = Button((744, 535, 124, 30), "Buy Units", self.buy, None,
                                        ((240, 255, 180), (160, 172, 110)),
                                        ((0, 0, 0), (160, 172, 110)))
        self.doneButton    = Button((1050, 660, 124, 30), "Next Turn", self.nextTurn, None,
                                        ((255,255,255), (0,0,0)),
                                        ((60, 60, 60), (0,0,0)))
                                        
        #Buy Buttons TEMP
        x = self.interface.width/2+self.interface.panelX+21
        y = self.interface.borders/2+self.interface.panelY+60
        w = 369
        h = 37
        c1 = ((240, 255, 180), (164, 168, 112))
        c2 = ((0,0,0), (164, 168, 112))
        self.buyPeasantButton = Button((x,y,w,h), "Recuit a Peasant (40 leons)", self.buyUnit, ('peasant', 40), c1, c2)
        y+=h+18
        self.buyBowmanButton = Button((x,y,w,h), "Recuit a Bowman (80 leons)", self.buyUnit, ('bowman', 80), c1, c2)
        y+=h+18
        self.buyKnightButton = Button((x,y,w,h), "Recuit a Knight (80 leons)", self.buyUnit, ('knight', 80), c1, c2)
        y+=h+18
        self.buyCatapultButton = Button((x,y,w,h), "Build a Catapult (80 leons)", self.buyUnit, ('catapult', 80), c1, c2)
        y+=h+18
        self.buySoldierButton = Button((x,y,w,h), "Recuit a Soldier (80 leons)", self.buyUnit, ('soldier', 80), c1, c2)
        y+=h+18
        self.buyCavalryButton = Button((x,y,w,h), "Train Cavalry (80 leons)", self.buyUnit, ('cavalry', 80), c1, c2)                      
        
        self.buttons = [self.attackButton, self.buyButton, self.doneButton,
                            self.buyPeasantButton, self.buyBowmanButton,
                            self.buyKnightButton, self.buyCatapultButton,
                            self.buySoldierButton, self.buyCavalryButton]
        
        self.buyButtons = [self.buyPeasantButton, self.buyBowmanButton,
                            self.buyKnightButton, self.buyCatapultButton,
                            self.buySoldierButton, self.buyCavalryButton]
        
        self.doneButton.setStatus(True)
        
        #Select a random player TEMP
        random.shuffle(self.board.players)
        self.currentPlayer = self.board.players[0]
        self.currentPlayerIndex = 0
        self.attackTarget = None
        self.buyTarget = None
        self.nextTurn()
    
    #nextTurn
    def nextTurn(self):
        if self.doneButton.active == True:
            self.latestSelection[self.currentPlayerIndex] = self.selected
            self.currentPlayerIndex = (self.currentPlayerIndex+1)%(len(self.board.players))
            self.currentPlayer = self.board.players[self.currentPlayerIndex]
            self.attackMove = 1
            self.buyMove = 1
            self.previous = None
            self.doneButton.setStatus(False)
            self.interface.instructColor = self.currentPlayer.colorValue
            self.doneButton.color[0] = self.currentPlayer.colorValue
            self.interface.setText("")
            self.selected=None
            pygame.time.delay(500)
            pygame.event.clear()
            self.interface.showInfo()
            try:
                if self.latestSelection[self.currentPlayerIndex].controller == self.currentPlayer:
                    self.selected = self.latestSelection[self.currentPlayerIndex]
                else:
                    raise Exception()
            except:
                for p in self.board.provinces:
                    if p.controller == self.currentPlayer:
                        self.selected = p
            
            #Add cash
            for p in self.board.provinces:
                if p.controller == self.currentPlayer:
                    self.currentPlayer.cash +=10
            self.interface.setCash(self.currentPlayer.cash)

            self.select()
            self.doneButton.setStatus(True)
            self.interface.setText(self.currentPlayer.name+"'s turn has begun.")

    
        
    #buyMove
    def buy(self):
        if self.buyButton.active == True:
            self.interface.setText("Buy a unit?")
            for b in self.buyButtons:
                b.setStatus(True)
            self.buyMove = 2
            self.buyTarget = self.selected
            self.interface.showBuyMenu()
            
    #buyAUnit
    def buyUnit(self, (unitType, cost)):
        
        #What can we build?
        l = []
        for r in self.board.resources:
            if r.province.controller == self.currentPlayer:
                l.append(r.rType.canProduce)
        ut = getUnitType(unitType)
    
        if self.selected.army.number == 5:
            self.interface.setText("There is no room left for units.")
            return False
        if ut not in l and not unitType == 'peasant':
            self.interface.setText("You lack resources to produce that unit.")
            return False            
        if self.currentPlayer.cash < cost:
            self.interface.setText("You cant afford that unit.")
            return False
        
        self.selected.army.units.append(Unit(ut))
        self.selected.army.update()
        self.interface.setText("Bought new a "+ut.name+"!")
        return True

    #AttackMove
    def attack(self):
        if self.attackButton.active == True:
            self.interface.setText("Select a adjacent province to attack.")
            self.attackMove = 2
    
    #AttackAction
    def attackAction(self, fromProvince, toProvince):
        attackingArmy = {0:None, 1:None, 2:None, 3:None, 4:None}
        defendingArmy = {0:None, 1:None, 2:None, 3:None, 4:None}
        
        #Shuffle armies
        if toProvince.army == None:
            toArmyLen = 0
        else:
            toArmyLen = toProvince.army.number
        order0 = list(range(max(fromProvince.army.number, toArmyLen)))
        order1 = list(order0)
        order2 = list(order0)
        random.shuffle(order1)
        random.shuffle(order2)
        i = 0        
        for u in fromProvince.army.units:
            attackingArmy[order1[i]] = u
            i+=1
        
        i = 0
        if toProvince.army != None:
            i = 0        
            for u in toProvince.army.units:
                defendingArmy[order2[i]] = u
                i+=1
        
        #Fight!
        for i in range(5):
            if attackingArmy[i] == None or defendingArmy[i] == None:
                continue
            if defendingArmy[i].uType in attackingArmy[i].uType.strongAgainst:
                defendingArmy[i].health -= 75
            else:
                defendingArmy[i].health -= 50
            if attackingArmy[i].uType in defendingArmy[i].uType.strongAgainst:
                attackingArmy[i].health -= 50
            else:
                attackingArmy[i].health -= 25           
        #Show report
        self.interface.showBattleReport(attackingArmy, defendingArmy)
    
        #Remove dead units
        if toProvince.army != None:
            toProvince.army.update()
        fromProvince.army.update()
        
        #Move to empty province
        if fromProvince.army.number > 0 and (toProvince.army == None or toProvince.army.number == 0):
            defendant = toProvince.controller
            toProvince.controller = self.currentPlayer
            self.interface.setText("Victory! The province '"+toProvince.name+"' was claimed.")
            
            
            #Delete player?
            remove = True
            for p in self.board.provinces:
                if p.controller == defendant:
                    remove = False
                    break
            if remove:
                self.board.players.remove(defendant)
                self.interface.setText(defendant.name+" has been destroyed!")
                if len(self.board.players) == 1:
                    print "VICTORY!!"

            if toProvince.army != None:
                self.board.armies.remove(toProvince.army)
            
            toProvince.addArmy(fromProvince.army)
            fromProvince.army = Army(fromProvince.flagX, fromProvince.flagY, fromProvince)
            self.board.armies.append(fromProvince.army)
            #Update flags again
            toProvince.army.update()
            fromProvince.army.update()
            #Successfull attack
            return True
        #unsuccessfull attack
        self.interface.setText("The province was not claimed.")
        return False

    #Main Game Loop
    def loop(self):
        
        #Sync frames.
        self.timer.tick(self.framerate)
            
        #Update mouse position.
        self.mousePosition = pygame.mouse.get_pos()
        
        #Get pressed keyboard buttons.
        self.keysPressed = pygame.key.get_pressed()

        #Get hovered object.
        self.hovered = self.idMap.get(self.mousePosition)

        #Update the id map
        self.idMap.update()
        
        #Change cursor.
        if self.hovered != None:
            pygame.mouse.set_cursor(*self.interface.linkCursor)
        else:
            pygame.mouse.set_cursor(*self.interface.pointerCursor)
            
        #Attack another province
        if self.attackMove == 2:
            for k, p in self.selected.neighbours.iteritems():
                if self.hovered == p and p.controller != self.currentPlayer:
                    pygame.mouse.set_cursor(*self.interface.targetCursor)
                    self.attackTarget = p
                    break
                            
        #Keyboard shortcuts
        if self.keysPressed[pygame.K_a]:
            self.attack()
        if self.keysPressed[pygame.K_b]:
            self.buy()
        if self.keysPressed[pygame.K_SPACE]:
            self.nextTurn()
                        
        #Events.
        for event in pygame.event.get():        
        
                #The Application quits.
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                    
                #The Mouse is pressed, select a map object.
                if event.type == MOUSEBUTTONDOWN:
                    self.previous = self.selected
                    self.selected = self.hovered                    
                    self.select()

        #Update and draw the interface
        self.interface.update()
        
        
        
   #Select a object 
    def select(self):
        self.attackButton.setStatus(False)
        self.buyButton.setStatus(False) 
        button = None                      
        
        
        if self.buyMove == 2:
            self.buyMove = 1
            for b in self.buyButtons:
                b.setStatus(False)
            self.interface.setText("")
        
        if self.attackMove == 2:
            if self.attackTarget != None and self.selected == self.attackTarget:
                self.attackMove = 0
                if not self.attackAction(self.previous, self.selected):
                    self.selected = self.previous
                return False
            else:
                self.attackMove = 1
        if self.selected.__class__.__name__ == "Button":
            button = self.selected
            self.selected = self.previous
            self.previous = None
        
        if self.selected.__class__.__name__ == "Province" and self.selected.controller == self.currentPlayer:
            if self.attackMove>0 and self.selected.army!=None and self.selected.army.number>0 and self.buyMove<2:
                self.attackButton.setStatus(True)
            if self.buyMove==1:
                self.buyButton.setStatus(True)                        
            
        if button != None:
            if button.args != None:
                button.function(button.args)
            else:
                button.function()
                    
        if self.buyMove>1:
            self.interface.showBuyMenu()
        else:
            self.interface.showInfo()
        return True