import pygame, os, sys, TextWrapping
from pygame.locals import *

from Singleton    import *
from IdMap        import *
from GameBoard    import *
from Screen import *


"""
Loads a cursors from the specified subfolder in 'cursors'. and returns it
"""
def loadCursor(folder):
    return pygame.cursors.load_xbm(
        os.path.join('data', 'cursors', folder, 'cursor.xbm'),
        os.path.join('data', 'cursors', folder, 'mask.xbm'))



"""
Class: Game Interface
A singelton class (allows for a global, single, instance of the class) that handles UI events and controls
draw operations.
"""
@Singleton
class GameInterface:
    
    def __init__(self):
         
        #Load images.
        self.backgroundImage = pygame.image.load(os.path.join('data', 'common', 'background', 'img.png'))
        self.panelImage      = pygame.image.load(os.path.join('data', 'common', 'panel', 'img.png'))
        self.unitImage       = pygame.image.load(os.path.join('data', 'common', 'panel', 'slot.png'))
        self.crossImage      = pygame.image.load(os.path.join('data', 'common', 'panel', 'cross.png'))
        self.arrowImage      = {'up':pygame.image.load(os.path.join('data', 'common', 'arrows', 'up.png')),
                                'up-left':pygame.image.load(os.path.join('data', 'common', 'arrows', 'upleft.png')),
                                'up-right':pygame.image.load(os.path.join('data', 'common', 'arrows', 'upright.png')),
                                'down':pygame.image.load(os.path.join('data', 'common', 'arrows', 'down.png')),
                                'down-left':pygame.image.load(os.path.join('data', 'common', 'arrows', 'downleft.png')),
                                'down-right':pygame.image.load(os.path.join('data', 'common', 'arrows', 'downright.png'))}
        self.unitsInfoImage  = pygame.image.load(os.path.join('data', 'common', 'unitsinfo', 'img.png'))
        #Load informations from the data folder.
        with open(os.path.join('data', 'game', 'information.txt'), 'r') as f:
            lines = f.readlines()
            
            #Size and position
            self.width   = int(lines[4].decode('utf8').strip('\n'))
            self.height  = int(lines[5].decode('utf8').strip('\n'))
            self.borders = int(lines[6].decode('utf8').strip('\n'))
            
            #Caption
            self.caption = lines[1].decode('utf8').strip('\n')
            f.close()
            
            #Advanced textformating (TEMP)
            self.titleSize = 30
            self.bodySize  = 24
            self.linkSize  = 22
            self.noteSize  = 18
            self.unitSize  = 15
            self.panelWidth = self.panelImage.get_width()
            self.buttonSize = 24
    
            self.panelX = 94
            self.panelY = 40
            
            self.xPadding = 10
            self.yPadding = 10
            
            self.noteOffset = 300
            self.linkOffset = 180
            
            self.unitOffset = 20
            self.unitMargin = 7
            
            self.healthbarOffset  = 60
            self.healthbarColor   = (255, 0, 0)
            self.healthbarBGColor = (255, 255, 255)
            self.healthbarWidth   = 50
            self.healthbarHeight  = 6
        
        #Load cursors.
        self.pointerCursor = loadCursor('pointer')
        self.linkCursor    = loadCursor('link')
        self.handCursor    = loadCursor('hand')
        self.holdCursor    = loadCursor('hold')
        self.targetCursor  = loadCursor('target')
    
        #Load fonts.
        self.titleFont  = pygame.font.Font(os.path.join('data', 'fonts', 'title', 'font.ttf'), self.titleSize)
        self.titleColor = (163, 167, 111)
        self.bodyFont   = pygame.font.Font(os.path.join('data', 'fonts', 'body', 'font.ttf'), self.bodySize)
        self.bodyColor  = (163, 167, 111)
        self.linkFont   = pygame.font.Font(os.path.join('data', 'fonts', 'link', 'font.ttf'), self.linkSize)
        self.linkColor  = (163, 167, 111)
        self.noteFont   = pygame.font.Font(os.path.join('data', 'fonts', 'note', 'font.ttf'), self.noteSize)
        self.noteColor  = (163, 167, 111)
        self.buttonFont = pygame.font.Font(os.path.join('data', 'fonts', 'button', 'font.ttf'), self.buttonSize)
        
        #Animation variables.
        self.animationStep  = 0
        self.animationSpeed = .5
        self.animationStop  = 2
        
        #Find the Gameboard and IdMap.
        self.board = GameBoard.Instance()
        self.idMap = IdMap.Instance()
        
        #Set display options and create it.
        pygame.display.set_caption(self.caption)
        pygame.mouse.set_visible(True)
        
        #Creates surfaces
        self.window     = pygame.display.set_mode((self.width, self.height+self.borders))
        self.background = pygame.Surface((self.width, self.height+self.borders))
        
        #Fill the background image
        self.background.blit(self.backgroundImage, (0, self.borders/2))
        self.background.blit(self.backgroundImage, (self.width/2, self.borders/2))
    
        #Prepare text drawing variables TEMP
        self.titleText     = None
        self.bodyText      = None
        self.noteText      = None
        self.linkText      = None
        self.displayInfo   = False
        self.instructionalText = None
        self.instructColor = (255, 255, 255)
        self.cashText = None
        
    #Updates the interface (draws it's components) and updates the id-map.
    def update(self):
                
        #Update animation
        self.animationStep = (self.animationStep+self.animationSpeed)%self.animationStop

        #Draw background
        self.window.blit(self.background, (0,0))
        
        #Draw map
        self.window.blit(self.board.mapImage, (0,self.board.yOffset))

        #Draw selected province and neighbour
        if self.manager.selected.__class__.__name__ == "Province":
            self.manager.selected.setAlpha(150)
            self.window.blit(self.manager.selected.image, (0,self.board.yOffset))
            for k, p in self.manager.selected.neighbours.iteritems():
                p.setAlpha(90)
                self.window.blit(p.image, (0,self.board.yOffset))
        if self.manager.selected.__class__.__name__ == "Resource":
            self.manager.selected.province.setAlpha(120)
            self.window.blit(self.manager.selected.province.image, (0,self.board.yOffset))
            
         
        #Draw borders
        self.window.blit(self.board.bordersImage, (0,self.board.yOffset))

        #Draw resources
        for r in self.board.resources:
            self.window.blit(r.rType.shadow, (r.x, r.y))
            if self.manager.selected == r:
                self.window.blit(r.rType.image, (r.x, r.y-self.animationStep))
            else:
                self.window.blit(r.rType.image, (r.x, r.y))
                
        #Draw flags
        for f in self.board.armies:
            self.window.blit(f.shadow, (f.x, f.y))
            if self.manager.selected == f.province:
                self.window.blit(f.image, (f.x, f.y-self.animationStep))
            else:
                self.window.blit(f.image, (f.x, f.y))

        #Draw info panel
        if self.displayInfo:
            self.drawInfo()
        
        #Draw buttons
        for b in self.manager.buttons:
            if b.active == True:
                if self.manager.hovered == b:
                    text = self.buttonFont.render(b.text, True, b.color[1])
                    b.image.fill(b.bgColor[1])
                else:            
                    text = self.buttonFont.render(b.text, True, b.color[0])
                    b.image.fill(b.bgColor[0])
                b.image.blit(text, (b.image.get_width()/2-text.get_width()/2, b.image.get_height()/2-text.get_height()/2)) 
                self.window.blit(b.image, (b.x, b.y))   

        #Draw instructional text
        if self.instructionalText != None:
            self.window.blit(self.instructionalText, (self.width/2-self.instructionalText.get_width()/2, 660))
        
        #Draw current money
        if self.cashText != None:
            self.window.blit(self.cashText, (40, 660))
        
        #Draw fullscreens
        for s in Screen.l:
            self.window.blit(s.image, (0,0))
        
        #Update display
        pygame.display.update()
        
    
    #Sets a instructional text
    def setText(self, text):
        self.instructionalText = self.buttonFont.render(text, True, self.instructColor)
    
    #Displays the cash of the current player
    def setCash(self, value):
        value = str(value)
        self.cashText = self.buttonFont.render("leons: "+value, True, self.instructColor)
    
    #Draws a panel containing information
    def drawInfo(self):
        pos = [self.width/2+self.panelX, self.borders/2+self.panelY]
        
        #Background
        self.window.blit(self.panelImage, pos)
        
        #Title
        pos[1] += self.yPadding
        if self.titleText != None:
            self.window.blit(self.titleText, (pos[0]+self.panelWidth/2-self.titleText.get_width()/2, pos[1]))
        
        #Link
        if self.linkText != None:
            self.window.blit(self.linkText, (pos[0]+self.panelWidth/2-self.linkText.get_width()/2, pos[1]+self.linkOffset))

        #Notice
        if self.noteText != None:
            self.window.blit(self.noteText, (pos[0]+self.panelWidth/2-self.noteText.get_width()/2, pos[1]+self.noteOffset))
                    
        #Body, Text Content
        pos[0] += self.xPadding
        pos[1] += self.titleSize+self.yPadding
        if self.bodyText != None:
            self.window.blit(self.bodyText, (pos[0], pos[1]))
        

            
    #Sets information
    def showInfo(self):
        self.titleText = None
        self.bodyText  = None
        self.noteText  = None
        self.linkText  = None
        
        #Sets display options depending on the object type displayed.
        if self.manager.selected == None:
            self.displayInfo = False
            return False
        
        #Provinces
        if self.manager.selected.__class__.__name__ == "Province":
            body = self.manager.selected.description
                        
            #Draw a link to the resource in this province.
            if self.manager.selected.resource != None:
                self.linkText = self.linkFont.render("Gives you access to "+self.manager.selected.resource.name, True, self.linkColor)

            #Draw information about a province that is empty.
            if self.manager.selected.controller == None:
                self.noteText = self.noteFont.render("No faction controls this province.", True, self.noteColor)
                            
            #Draw units when the current player controls this province.
            elif self.manager.selected.controller == self.manager.currentPlayer:
                w = (self.unitImage.get_width())*5 + self.unitMargin*3+12
                h = self.unitImage.get_height()
                
                self.noteText = pygame.Surface((w, h), SRCALPHA, 32).convert_alpha()

                x = 0
                y = 0
                for i in range(1,6):
                    self.noteText.blit(self.unitImage, (x,y))
                    x+=self.unitImage.get_width()+self.unitMargin
                    
                x = self.unitImage.get_width()/2
                y = self.unitOffset          
                for unit in self.manager.selected.army.units:
                    
                    self.noteText.blit(unit.uType.image, (x-unit.uType.image.get_width()/2, y))
                    
                    pygame.draw.rect(self.noteText, self.healthbarBGColor,
                                        (x-self.healthbarWidth/2, y+self.healthbarOffset, self.healthbarWidth, self.healthbarHeight))
                    pygame.draw.rect(self.noteText, self.healthbarColor,
                                        (x-self.healthbarWidth/2, y+self.healthbarOffset, self.healthbarWidth*(unit.health/100.00), self.healthbarHeight))
                    
                    x+=self.unitImage.get_width()+self.unitMargin

            #Draw information about a province that is controlled by an enemy.
            else:
                name   = self.manager.selected.controller.name
                number = str(len(self.manager.selected.army.units))
                self.noteText = self.noteFont.render(name+"'s army consists of "+number+" units.", True, self.noteColor)
               
        #Resources
        if self.manager.selected.__class__.__name__ == "Resource":
            title = self.manager.selected.name
            body  = self.manager.selected.rType.description
            self.linkText = self.unitsInfoImage

        #Title.
        title = self.manager.selected.name
        self.titleText  = self.titleFont.render(title, True, self.titleColor)
       
        #Wrap body text
        body = TextWrapping.wrap_multi_line(body, self.bodyFont, self.panelWidth-self.xPadding*2)
        w = 0
        h = 0
        for l in body:
            w = max(w, self.bodyFont.size(l)[0])
            h += self.bodyFont.get_linesize()
        self.bodyText = pygame.Surface((w, h), SRCALPHA, 32).convert_alpha()
        h = 0
        for l in body:
            t = self.bodyFont.render(l, True, self.bodyColor)
            self.bodyText.blit(t, (0, h))
            h += self.bodyFont.get_linesize()
                
        #Show information.
        self.displayInfo = True
        return True
    
    
    
        
        
    #Buy Menu
    def showBuyMenu(self):    
        self.titleText = None
        self.bodyText  = None
        self.noteText  = None
        self.linkText  = None
        
        self.displayInfo = True 
        #Title.
        title = "Buy units in "+self.manager.selected.name+":"
        self.titleText  = self.titleFont.render(title, True, self.titleColor)
    
    
    
    #Battle Report
    def showBattleReport(self, attackingArmy, defendingArmy, attackResult, defenseResult):
        self.titleText = None
        self.bodyText  = None
        self.noteText  = None
        self.linkText  = None
        
        self.displayInfo = True        
        
        #Title.
        title = "Battle Results:"
        self.titleText = self.titleFont.render(title, True, self.titleColor)
        
        w = (self.unitImage.get_width())*5 + self.unitMargin*4+24
        h = self.unitImage.get_height()*3+24
                
        self.bodyText = pygame.Surface((w, h), SRCALPHA, 32).convert_alpha()

        x = 24+self.unitImage.get_width()/2
        y = 24
        for i in range(5):
            self.bodyText.blit(self.unitImage, (x-self.unitImage.get_width()/2,y))
            
            #Arrows
            if (attackResult[i] == 1):
                self.bodyText.blit(self.arrowImage['down'], (x-self.arrowImage['down'].get_width()/2,y+115))
            if (attackResult[i] == 2):
                self.bodyText.blit(self.arrowImage['down-left'], (x-self.arrowImage['down-left'].get_width()/2,y+115))
            if (attackResult[i] == 3):
                self.bodyText.blit(self.arrowImage['down-right'], (x-self.arrowImage['down-right'].get_width()/2,y+115))
            
            if (defenseResult[i] == 1):
                self.bodyText.blit(self.arrowImage['up'], (x-self.arrowImage['up'].get_width()/2,y+150))
            if (defenseResult[i] == 2):
                self.bodyText.blit(self.arrowImage['up-left'], (x-self.arrowImage['up-left'].get_width()/2,y+150))
            if (defenseResult[i] == 3):
                self.bodyText.blit(self.arrowImage['up-right'], (x-self.arrowImage['up-right'].get_width()/2,y+150))
            
            self.bodyText.blit(self.unitImage, (x-self.unitImage.get_width()/2,y+200))
            if attackingArmy[i] != None:
                y2 = y+self.unitOffset
                unit = attackingArmy[i]
                self.bodyText.blit(unit.uType.image, (x-unit.uType.image.get_width()/2, y2))
                pygame.draw.rect(self.bodyText, self.healthbarBGColor,
                                (x-self.healthbarWidth/2, y2+self.healthbarOffset, self.healthbarWidth, self.healthbarHeight))
                if unit.health>0:
                    pygame.draw.rect(self.bodyText, self.healthbarColor,
                                (x-self.healthbarWidth/2, y2+self.healthbarOffset, self.healthbarWidth*(unit.health/100.00), self.healthbarHeight))
                if unit.health<=0:
                    self.bodyText.blit(self.crossImage, (x-self.crossImage.get_width()/2, y2+10))
                    
            if defendingArmy[i] != None:
                y2 = y+self.unitOffset+200
                unit = defendingArmy[i]
                self.bodyText.blit(unit.uType.image, (x-unit.uType.image.get_width()/2, y2))
                pygame.draw.rect(self.bodyText, self.healthbarBGColor,
                                (x-self.healthbarWidth/2, y2+self.healthbarOffset, self.healthbarWidth, self.healthbarHeight))
                if unit.health>0:
                    pygame.draw.rect(self.bodyText, self.healthbarColor,
                                (x-self.healthbarWidth/2, y2+self.healthbarOffset, self.healthbarWidth*(unit.health/100.00), self.healthbarHeight))
                if unit.health<=0:
                    self.bodyText.blit(self.crossImage, (x-self.crossImage.get_width()/2, y2+10))
                    
            x+=self.unitImage.get_width()+self.unitMargin