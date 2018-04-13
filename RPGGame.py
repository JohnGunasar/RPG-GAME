from functools import partial
import subprocess
import pygame
import random
import random
import time
import json
import math



pygame.init()
gold = 0
xp = 0
display_width = 1024
display_height = 768
scrollSurface = pygame.display.set_mode((512,512))

def distance(x1,y1,x2,y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

class Button():

    text = str()
    x = int()
    y = int()
    width = int()
    height = int()
    inactive_color = None
    active_color = None
    action = str()
    active = bool()
    
    def __init__(self,text,x,y,width,height,inactive_color,active_color,action,text_color,text_size,active):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.inactive_color = inactive_color
        self.active_color = active_color
        self.action = action
        self.text_color = text_color
        self.text_size = text_size
        self.active = active

    def nothing():
        pass
        
    def handle_event(self,event):
        
        if self.is_hovered() and event.type == pygame.MOUSEBUTTONDOWN:
            self.action()
    
    def text_to_button(self,surface):
        textSurf, textRect = text_objects(self.text,self.text_color,self.text_size)
        textRect.center = ((self.x+(self.width/2)), self.y+(self.height/2))
        surface.blit(textSurf, textRect)

        
    def is_hovered(self):
        cur = pygame.mouse.get_pos()
        return self.x + self.width > cur[0] > self.x and self.y + self.height > cur[1] > self.y

    def drawButton(self, surface):

        if self.active:
            pygame.draw.rect(surface,self.inactive_color,[self.x,self.y,self.width,self.height])
            
        if self.is_hovered() and self.active:
            pygame.draw.rect(surface, self.active_color,[self.x,self.y,self.width,self.height])
        
        self.text_to_button(surface)

class Quest():

    #showIntro = bool()
    #description = str()
    #descX = int()
    #descY = int()
    #questStarted = bool()
    #questFinished = bool()
    #description2 = str()
    #description3 = str()
    #description4 = str()

    def __init__(self,showIntro,description,descX,descY,questStarted,questFinished,description2,description3,description4):
        self.showIntro = showIntro
        self.description = description
        self.descX = descX
        self.descY = descY
        self.questStarted = questStarted
        self.questFinished = questFinished
        self.description2 = description2
        self.description3 = description3
        self.description4 = description4

    def describeQuest(self,description,descX,descY,description2,description3,description4):
        if self.showIntro == True:
            alt_med_pos_message_to_screen(self.description,black,self.descX,self.descY,size = "altMed")
            alt_med_pos_message_to_screen(self.description2,black,self.descX,self.descY+35,size = "altMed")
            alt_med_pos_message_to_screen(self.description3,black,self.descX,self.descY+60,size = "altMed")
            alt_med_pos_message_to_screen(self.description4,black,self.descX,self.descY+85,size = "altMed")

    def startQuest(self):
        self.questStarted = True
        self.showIntro = False

    def finishQuest(self):
        self.questFinished = True
        self.showIntro = False

    def questShowDialogue(self):
       self.showIntro = True

class Game_Object():

    damage = int()
    health = int()
    acceleration_x = int()
    acceleration_y = int()
    image = ()
    startX = int()
    startY = int()
    game_Objects = []
    projectile = str()
    imageDirection = str()
    imageFront = str()
    imageBack = str()
    imageLeft = str()
    imageRight = str()

    def __init__(self,d,h,a_x,a_y,img,sX,sY,pj):
        self.damage = d
        self.health = h
        self.acceleration_x = a_x
        self.acceleration_y = a_y
        self.image = img
        self.startX = sX
        self.startY = sY
        self.projectile = pj
        game_Objects.append(self)

    def load(self,image):
        pygame.image.load(self.image)

    def spawn(self,startX,startY):
        gameDisplay.blit(self.load(image),[startX,startY])

class Enemy(Game_Object):

    AI_cur_x = int()
    AI_cur_y = int()
    
    topLeftBound = (())
    topRightBound = (())
    
    bottomLeftBound = (())
    bottomRightBound = (())
    
    topLeftBound_x = int()
    topLeftBound_y = int()
    
    topRightBound_x = int()
    topRightBound_y = int()
    
    bottomLeftBound_x = int()
    bottomLeftBound_y = int()
    
    bottomRightBound_x = int()
    bottomRightBound_y = int()
    
    def __init__(self,tlbx,tlby,trbx,trby,blby,blbx,brbx,brby,damage,health,acceleration_x,acceleration_y,image,startX,startY,projectile):
        super.__init__(damage,health,acceleration_x,acceleration_y,image,startX,startY,projectile)
        self.topLeftBound = ((tlbx,tlby))
        self.topRightBound = ((trbx,trby))
        self.bottomLeftBound = ((blbx,blby))
        self.bottomRightBound = ((brbx,brby))

    def bound(self,topLeftBound_x,topLeftBound_y,topRightBound_x,topRightBound_y,bottomLeftBound_x,bottomLeftBound_y,bottomRightBound_x,bottomRightBound_y):
        topLeftBound = ((self.topLeftBound_x,self.topLeftBound_y))
        topRightBound = ((self.topRightBound_x,self.topRightBound_y))
        bottomLeftBound = ((self.bottomLeftBound_x,self.bottomLeftBound_y))
        bottomRightBound = ((self.bottomRightBound_x,self.bottomRightBound_y))

    def pickRandomDirection(self,AI_cur_x,AI_cur_y):
        directions = ["left","right","down","up"]
        return directions[random.randint(0,3)]
                      
    def show(self,image):
        gameDisplay.blit(self.load(self.image),[self.AI_cur_x,self.AI_cur_y])
    
    def moveRandom(self,image,topLeftBound,topRightBound,bottomLeftBound,bottomRightBound,acceleration):
        
        gameExit = False
        while not gameExit:
            for event in pygame.event.get():
                direction = self.pickRandomDirection()

                midPoint1 = midPoint(topLeftBound_x,topRight_Bound_x,topLeftBound_y,topRightBound_y)
                midPoint1_x,midPoint1_y = midPoint1[0],midPoint1[1]

                midPoint2 = midPoint(bottomLeftBound_x,bottomRightBound_x,bottomLeftBound_y,bottomRightBound_y)
                midPoint2_x,midPoint2_y = midPoint2[0],midPoint2[1]
            
                if direction.equals("left") and distance(self.AI_cur_x,self.AI_cur_y,self.topLeftBound_x,self.topLeftBound_y) < distance(self.AI_cur_x,self.AI_cur_y,self.bottomLeftBound_x,self.bottomLeftBound_y) and distance(self.AI_cur_x,self.AI_cur_y,self.topLeftBound_x,self.topLeftBound_y) < acceleration:
                    self.AI_cur_x -= self.acceleration_x
                    self.AI_cur_y -= self.acceleration_y
                    self.show(self.image,self.AI_cur_x,self.AI_cur_y)
                   
                elif direction.equals("left") and distance(self.AI_cur_x,self.AI_cur_y,self.topLeftBound_x,self.topLeftBound_y) > distance(self.AI_cur_x,self.AI_cur_y,self.bottomLeftBound_x,self.bottomLeftBound_y) and distance(self.AI_cur_x,self.AI_cur_y,self.bottomLeft_x,self.bottomLeftBound_y) < acceleration:
                    self.AI_cur_x -=self.acceleration_x
                    self.AI_cur_y += self.acceleration_y
                    self.show(self.image,self.AI_cur_x,self.AI_cur_y)

                elif direction.equals("right") and distance(self.AI_cur_x,self.AI_cur_y,self.topRightBound_x,self.topRightBound_y) < distance(self.AI_cur_x,self.AI_cur_y,self.bottomRightBound_x,self.bottomRightBound_y) and distance(self.AI_cur_x,self.AI_cur_y,self.topRightBound_x,self.topRightBound_y) < acceleration:
                    self.AI_cur_x += self.acceleration_x
                    self.AI_cur_y -= self.acceleration_y
                    self.show(self.image,self.AI_cur_x,self.AI_cur_y)

                elif direction.equals("right") and distance(self.AI_cur_x,self.AI_cur_y,self.topRightBound_x,self.topRightBound_y) > distance(self.AI_cur_x,self.AI_cur_y,self.bottomRightBound_x,self.bottomRightBound_y) and distance(self.AI_cur_x,self.AI_cur_y,self.bottomRightBound_x,self.bottomRightBound_y) < acceleration:
                    self.AI_cur_x += acceleration_x
                    self.AI_cur_y += self.acceleration_y
                    self.show(self.image,self.AI_cur_x,self.AI_cur_y))

                elif direction.equals("up") and distance(0,self.AI_cur_y,0,self.topLeftBound_y) < acceleration and distance(0,self.AI_cur_y,0,self.RightBound_y) < acceleration:
                    self.AI_cur_x += 0
                    self.AI_cur_y -= acceleration
                    self.show(self.image,self.AI_cur_x,self.AI_cur_y))

                elif direction.equals("down") and distance(0,self.AI_cur_y,0,self.bottomLeftBound_y) < acceleration and distance(0,self.AI_cur_y,0,self.bottomRightBound_y) < acceleration:
                    self.AI_cur_x += 0
                    self.AI_cur_y += acceleration
                    self.show(self.image,self.AI_cur_x,self.AI_cur_y)

                else:
                    self.pickRandomDirection
                                                                                                                                                                                                                                                                                                                           
class Player(Game_Object):
    pass
         
Quest1 = Quest(False,"Hello adventurer!",200,300,False,False,"for your first quest I need you to click that button for me","I will give you 100 gold pieces for this","")
Quest2 = Quest(False,"I am hungry",200,300,False,False,"Go get a porkchop from that piggy for me "," better be quick, I get hangry","")                
global health
global points
health = 0
points = 25



backgroundImg = 'C:/Users/student/Desktop/Stuff/Programming/Python/Projects/Game/Images/BackGround.jpg'
dungeonImg = 'C:/Users/student/Desktop/Stuff/Programming/Python/Projects/Game/Images/dungeon.jpg'
buttonImg = 'C:/Users/student/Desktop/Stuff/Programming/Python/Projects/Game/Images/ButtonTexture.png'
wizImg = 'C:/Users/student/Desktop/Stuff/Programming/Python/Projects/Game/Images/wizard.png'
grassImg = 'C:/Users/student/Desktop/grass1.png'
dirtImg = 'C:/Users/student/Desktop/dirttile.png'
waterImg = 'C:/Users/student/Desktop/Stuff/Programming/Python/Projects/Game/Images/watertile.jpg'
sandImg = 'C:/Users/student/Desktop/Stuff/Programming/Python/Projects/Game/Images/sandtile.jpg'
treeImg = 'C:/Users/student/Desktop/flowers.png'
questGiverImg = 'C:/Users/student/Desktop/Stuff/Programming/Python/Projects/Game/Images/NPC.png'
scrollImg = 'C:/Users/student/Desktop/Stuff/Programming/Python/Projects/Game/Images/scroll.png'
npcPromptImg = 'C:/Users/student/Desktop/Stuff/Programming/Python/Projects/Game/Images/NPCPROMPT.png'
#pigImg = 'C:/Users/student/Desktop/Stuff/Programming/Python/Projects/Game/Images/pig/pig.png'
heartImg = 'C:/Users/student/Desktop/Stuff/Programming/Python/Projects/Game/Images/heart.png'
swordImg = 'C:/Users/student/Desktop/Stuff/Programming/Python/Projects/Game/Images/sword.png'
shieldImg = 'C:/Users/student/Desktop/Stuff/Programming/Python/Projects/Game/Images/shield.png'
sword2Img = 'C:/Users/student/Desktop/Stuff/Programming/Python/Projects/Game/Images/sword2.png'
borderImg = 'C:/Users/student/Desktop/Stuff/Programming/Python/Projects/Game/Images/border.png'
charImg = 'C:/Users/student/Desktop/Stuff/Programming/Python/Projects/Game/Images/Character.png'
attackAnim = 'C:/Users/student/Desktop/Stuff/Programming/Python/Projects/Game/Images/FINALANIMATION.png'
pigHurt = 'C:/Users/student/Desktop/Stuff/Programming/Python/Projects/Game/Images/pig/pig2anim.png'
#fullPig = 'C:/Users/student/Desktop/Stuff/Programming/Python/Projects/Game/Images/pig/NotBeingDamaged/fullHeartpig.png'
FourToTwo = 'C:/Users/student/Desktop/Stuff/Programming/Python/Projects/Game/Images/pig/Sprite Sheets/threefourthpig.png'
Half = 'C:/Users/student/Desktop/Stuff/Programming/Python/Projects/Game/Images/pig/NotBeingDamaged/pigHalfheart.png'
InvPaper = 'C:/Users/student/Desktop/Stuff/Programming/Python/Projects/Game/Images/invPaper.png'
FullDead = 'C:/Users/student/Desktop/Stuff/Programming/Python/Projects/Game/Images/pig/Sprite Sheets/completelyDead.png'
FullDead2 = 'C:/Users/student/Desktop/Stuff/Programming/Python/Projects/Game/Images/pig/Sprite Sheets/completelyDead2.png'
PathTrimming = 'C:/Users/student/Desktop/pathTrimming.png'
PathTrimming1 = 'C:/Users/student/Desktop/pathTrimming1.png'
PathTrimming2 = 'C:/Users/student/Desktop/pathTrimming2.png'
PathTrimming3 = 'C:/Users/student/Desktop/pathTrimming3.png'
PathTrimming4 = 'C:/Users/student/Desktop/pathTrimming4.png'
TreeStump1 = 'C:/Users/student/Desktop/treeStump1.png'
TreeStump2 = 'C:/Users/student/Desktop/treeStump2.png'
PathTrimming5 = 'C:/Users/student/Desktop/pathTrimming5.png'
PathTrimming6 = 'C:/Users/student/Desktop/pathTrimming6.png'
TreeOneBottomLeft = 'C:/Users/student/Desktop/Tree/Tree One Bottom Left.png'
TreeOneBottomRight = 'C:/Users/student/Desktop/Tree/Tree One Bottom Right.png'
TreeOneTopLeft = 'C:/Users/student/Desktop/Tree/Tree One Top Left.png'
TreeOneTopRight = 'C:/Users/student/Desktop/Tree/Tree One Top Right.png'    
DirtWall1 = 'C:/Users/student/Desktop/dirtWall1.png'
DirtWall2 = 'C:/Users/student/Desktop/dirtWall2.png'
DirtWall3 = 'C:/Users/student/Desktop/dirtWall3.png'
DirtWall4 = 'C:/Users/student/Desktop/dirtWall4.png'
Water1 = 'C:/Users/student/Desktop/water1.png'
Water2 = 'C:/Users/student/Desktop/water2.png'
Water3 = 'C:/Users/student/Desktop/water3.png'
Water4 = 'C:/Users/student/Desktop/water4.png'
B1 = 'C:/Users/student/Desktop/b1.png'
B2 = 'C:/Users/student/Desktop/b2.png'
B3 = 'C:/Users/student/Desktop/b3.png'
D2 = 'C:/Users/student/Desktop/d2.png'
TD1 = 'C:/Users/student/Desktop/td1.png'
TD2 = 'C:/Users/student/Desktop/td2.png'
PostBox = 'C:/Users/student/Desktop/postbox.png'
PB1 = 'C:/Users/student/Desktop/pb1.png'
PB2 = 'C:/Users/student/Desktop/pb2.png'
PB3 = 'C:/Users/student/Desktop/pb3.png'
PB4 = 'C:/Users/student/Desktop/pb4.png'
TD3 = 'C:/Users/student/Desktop/td3.png'
TD4 = 'C:/Users/student/Desktop/td4.png'
tS1 = 'C:/Users/student/Desktop/ts1.png'
tS2 = 'C:/Users/student/Desktop/ts2.png'
tS3 = 'C:/Users/student/Desktop/ts3.png'
tS4 = 'C:/Users/student/Desktop/ts4.png'
tS5 = 'C:/Users/student/Desktop/ts5.png'
tS6 = 'C:/Users/student/Desktop/ts6.png'
tS7 = 'C:/Users/student/Desktop/ts7.png'
tS8 = 'C:/Users/student/Desktop/ts8.png'
bugFront = 'C:/Users/student/Desktop/bug.png'
bugBack = 'C:/Users/student/Desktop/bugback.png'




gameDisplay = pygame.display.set_mode((display_width,display_height))

pygame.display.set_caption('Rocky')
pygame.display.update()

white = (255,255,255,)
transparentWhite = pygame.Color(255,255,255,50)
opaqueWhite = pygame.Color(255,255,255,127)
black = (0,0,0)
light_red = (255,0,0)
red = (200,0,0)
green = (34,177,76)
light_green = (0,255,0)
titleColor = (102,153,217)
light_blue = (0,0,255)
blue = (10,10,225)
yellow = (255,255,0)
light_yellow = (215,195,15)
clock = pygame.time.Clock()

g1 = (30,170,90)
g2 = (20,160,90)
g3 = (30,170,45)
g4 = (30,120,0)
g5 = (60,240,60)

d1 = (50,18,18)
d2 = (75,9,9)
d3 = (100,25,25)

w1 = (10,25,225)
s1 = (225,225,0)
s2 = (200,200,0)

blue = (0,0,200)
light_blue = (0,0,255)

smallfont = pygame.font.SysFont("Algerian", 25)
medfont = pygame.font.SysFont("Algerian", 50)
largefont = pygame.font.SysFont("Algerian", 85)

altSmall = pygame.font.SysFont("Algerian",20)
altMed = pygame.font.SysFont("Algerian",30)
altLarge = pygame.font.SysFont("Algerian",75)


def text_objects(text, color,size = "small"):

    if size == "small":
        textSurface = smallfont.render(text, True, color)
    if size == "medium":
        textSurface = medfont.render(text, True, color)
    if size == "large":
        textSurface = largefont.render(text, True, color)

    if size == "altMed":
        textSurface = altMed.render(text,True,color)

    if size == "altSmall":
        textSurface = altSmall.render(text,True,color)

    if size == "medFont":
        textSurface = medfont.render(text,True,color)

    if size == "smallFont":
        textSurface = smallfont.render(text,True,color)

    return textSurface, textSurface.get_rect()
   
def message_to_screen(msg,color, y_displace = 0, size = "small"):
    textSurf, textRect = text_objects(msg,color,size)
    textRect.center = (int(display_width / 2), int(display_height / 2)+y_displace)
    gameDisplay.blit(textSurf, textRect)

def alt_message_to_screen (msg,color,x,y):
    textSurf,textRect = text_objects(msg,color,size)
    gameDisplay.blit(textSurf,textRect)

def small_pos_message_to_screen(msg,color,x,y,size = "small"):

    screen_text = smallfont.render(msg,True,color)
    gameDisplay.blit(screen_text,[x,y])

def med_pos_message_to_screen(msg,color,x,y,size = "medium"):
    screen_text = medfont.render(msg,True,color)
    gameDisplay.blit(screen_text,[x,y])

def large_pos_message_to_screen(msg,color,x,y,size = "large"):
    screen_text = largefont.render(msg,True,color)
    gameDisplay.blit(screen_text,[x,y])


def alt_small_pos_message_to_screen(msg,color,x,y,size = "altSmall"):
    screen_text = altSmall.render(msg,True,color)
    gameDisplay.blit(screen_text,[x,y])
    
def alt_med_pos_message_to_screen(msg,color,x,y,size = "altMed"):
    screen_text = altMed.render(msg,True,color)
    gameDisplay.blit(screen_text,[x,y])

def alt_large_pos_message_to_screen(msg,color,x,y,size = "altLarge"):
    screen_text = altLarge.render(msg,True,color)
    gameDisplay.blit(screen_text,[x,y])

def pause():

    global health
    health = 0
    paused = True
    message_to_screen("Paused",black,-100,size="large")
    message_to_screen("Press C to continue playing or Q to quit",black,25)
    pygame.display.update()
    while paused:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        paused = False
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        quit()           
        clock.tick(5)

pygame.key.set_repeat(10,10)
def game_intro():

    intro = True

    startGame = Button("Start Game",50,425,350,75,red,light_red,gameLoop,black,"smallFont",True)
    
    while intro:
        t0 = time.time()
        for event in pygame.event.get():
            startGame.handle_event(event)
            if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    intro = False
                    gameLoop()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

                elif event.key == pygame.K_c:
                    characterCreation()
                    intro = False

                elif event.key == pygame.K_F11:
                    pygame.display.set_mode((display_width,display_height),pygame.FULLSCREEN)
        backImg = pygame.image.load(backgroundImg)
        gameDisplay.blit(backImg,[0,0])
        message_to_screen("Rocky",green,-100,size="large")
        startGame.drawButton(gameDisplay)
        pygame.display.update()
        clock.tick(60)

def nothing():   
    pass

def Quest1Func():
   global gold
   global xp
   global level
   border = pygame.image.load(borderImg)
   questDisplay = pygame.display.set_mode((display_width,display_height))
   questDisplay.fill((255,0,0))
   finishQuest1 = Button("Finish Quest",200,410,150,80,blue,light_blue,Quest1.finishQuest,black,"altSmall",False)
   finishQuest1.active = True
   while Quest1.showIntro:
      for event in pygame.event.get():
         finishQuest1.handle_event(event)
         if event.type == pygame.QUIT:
            pygame.quit()
            quit()
      finishQuest1.drawButton(questDisplay)
      #print("Running Quest1Func")
      questDisplay.blit(border,[30,30])
      Quest1.describeQuest(Quest1.description,Quest1.descX,Quest1.descY,Quest1.description2,Quest1.description3,Quest1.description4)
      if Quest1.questFinished:
          gold += 100
          xp += 100
          
      clock.tick(30)
      pygame.display.update()
def Quest2Func():
   border = pygame.image.load(borderImg)
   questDisplay = pygame.display.set_mode((display_width,display_height))
   startQuest2 = Button("Start Quest",200,410,150,80,blue,light_blue,Quest2.startQuest,black,"altSmall",True)
   questDisplay.fill((255,0,0))
   while Quest2.showIntro:
      for event in pygame.event.get():
         startQuest2.handle_event(event)
         if event.type == pygame.QUIT:
            pygame.quit()
            quit()
            
      questDisplay.blit(border,[30,30])
      Quest2.describeQuest(Quest2.description,Quest2.descX,Quest2.descY,Quest2.description2,Quest2.description3,Quest2.description4)
      startQuest2.drawButton(gameDisplay)
      clock.tick(30)
      pygame.display.update()

def inventory(gold,xp,level):

    timer = pygame.time.Clock()

    goldButton = Button("Gold: " + str(gold),50,50,150,75,red,light_red,nothing,black,"small",True)
    xpButton = Button("Xp: " + str(xp),50,150,125,75,red,light_red,nothing,black,"small",True)
    levelButton = Button("Level: " + str(level),50,250,150,75,red,light_red,nothing,black,"small",True)
    Resume = Button("Resume",50,200,85,40,yellow,light_yellow,gameLoop,black,"altSmall",True)
    inInv = True
    while inInv:
        for event in pygame.event.get():
            goldButton.handle_event(event)
            xpButton.handle_event(event)
            levelButton.handle_event(event)
            Resume.handle_event(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    return
                
        gameDisplay.fill(blue)
        invPaper = pygame.image.load(InvPaper)
        gameDisplay.blit(invPaper,[0,0])
        alt_med_pos_message_to_screen("Gold: " + str(gold),black,50,50,size = "altMed")
        alt_med_pos_message_to_screen("Xp: " + str(xp),black,50,100,size = "altMed")
        alt_med_pos_message_to_screen("Level: " + str(level),black,50,150,size = "altMed")
        alt_med_pos_message_to_screen("In Progress: ",black,700,400,size = "altMed")
        
        alt_med_pos_message_to_screen("Finished Quests: ",black,700,60,size = "altMed")

        Resume.drawButton(gameDisplay)

        if Quest1.questFinished:
            alt_med_pos_message_to_screen("Quest 1 finished",black,700,100,size = "altMed")

        if Quest2.questStarted:
            alt_med_pos_message_to_screen("Quest 2 in progress",black,700,440,size = "altMed")

        #goldButton.drawButton(gameDisplay)
        #xpButton.drawButton(gameDisplay)
        #levelButton.drawButton(gameDisplay)
        timer.tick(60)
        pygame.display.update()
    
def gameLoop():
    sw = int()
    sh = int()
    
    frontBug = pygame.image.load(bugFront)
    backBug = pygame.image.load(bugBack)
    halfHealth = pygame.image.load(Half)
    hitCounter = 0
    pigX = 100
    pigY = 300
    bugX = 100
    bugY = 300

    

    def lootPig():
        lootDisplay = True
        while lootDisplay:

            for evt in pygame.event.get():
                if evt.type == pygame.KEYDOWN:
                    if evt.key == pygameK_s:
                        lootDisplay = False
                        gameLoop()

            lootTable.fill(red)
            pygame.display.update()

            

    pigLoot = Button("Loot",pigX + 25,pigY-60,100,40,red,light_red,lootPig,black,"altSmall",True)
    
    def sprite( sw, sh,sprite_sheet,surface,x,y,frames):
        
        animation_frames = []
        timer = pygame.time.Clock()
        image = pygame.image.load(sprite_sheet).convert_alpha()
        frameCounter = 0
        
        for i in range( 0,frames ):
            animation_frames.append( image.subsurface( ( 0, i * sw, sh, sw ) ) )

        counter = 0

        while frameCounter <= frames:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or ( event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE ) :
                    sys.exit()
                    
            surface.blit( animation_frames[counter], ( x  , y  ) )
            counter = ( counter + 1 ) % 2
            pygame.display.update()
            frameCounter += 1
            timer.tick(60)
            
    #image = pygame.image.load(attackAnim).convert_alpha()
    #animation_frames = []
    #for i in range(0, 2):
     #       animation_frames.append( image.subsurface( ( 0, i * 100, 100, 100 ) ) )
            #charImg = animation_frames[i]

    #isIdle = True
    #isAttacking = False
    #attackFrame = 0
    #def blitChar(surface, x, y):
     #   nonlocal isAttacking,isIdle,attackFrame 
      #  print(isAttacking, " Is attacking")
       # print(isIdle, "Is idle")
        #if attackFrame == 2:
         #   isAttacking = False
          #  isIdle = True
           # attackFrame = 0
            
        #sprite = animation_frames[0] #???
        #sprite_index = 0
        #if isAttacking:
            #sprite = animation_frames[attackFrame]
         #   sprite_index = attackFrame
          #  attackFrame += 1
        #surface.blit(animation_frames[sprite_index], [x, y])

    global gold
    global xp
    global level
    x = display_width / 2
    y = display_height / 2
    npcX = 384
    npcY = 236
    npcDirection = "right"
    npcDirY = "up"
    pigXDir = "right"
    pigYDir = "up"
    pigStop = "move"
    pigDead = False
    gameExit = False
    level = 0
    bugDirX = "right"
    bugDirY = "up"
    
    t0 = time.time()
    
    while not gameExit:
        quest1Button = Button("Quest 1",700,200,200,80,red,light_red,Quest1.questShowDialogue,black,"altSmall",False)
        quest2Button = Button("Quest 2",100,100,200,80,red,light_red,Quest2.questShowDialogue,black,"altSmall",False)
        isAttacking = False
        for event in pygame.event.get():
            
            quest1Button.handle_event(event)
            quest2Button.handle_event(event)
            pigLoot.handle_event(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    y -= 20

                if event.key == pygame.K_s:
                    y += 20

                if event.key == pygame.K_a:
                    x -= 20

                if event.key == pygame.K_d:
                    x += 20

                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

                if xp >= 100 and xp < 500:
                    level = 1

                if event.key == pygame.K_i:
                    inventory(gold,xp,level)
                    if xp >= 100:
                        level = 1

                if event.key == pygame.K_F11:

                    pygame.display.set_mode((display_height,display_width),pygame.FULLSCREEN)

                if event.key == pygame.K_e:
                    sprite( 100, 100,attackAnim,gameDisplay,x,y,2)
                    isAttacking = True

                        #if not pigDead and hitCounter == 1 and pygame.K_e and distance(x,y,pigX,pigY)<=150:
                    #print("Half Health")
                 #   pig = halfHealth
                    #gameDisplay.blit(halfHealth,[pigX,pigY])

#                if hitCounter == 2 and pygame.K_e and distance(x,y,pigX,pigY)<=150:
 #                   pigDead = True
  #                  pig = deadPig
   #                 attackPig = pig
    #                hitCounter = 0
     #               print("Pig ",hex(id(pig)))
      #              print("Attack Pig ",hex(id(attackPig)))

                #if pigDead and pygame.K_e and distance(x,y,pigX,pigY) <= 150:
                 #   gameDisplay.blit(deadPig,[pigX,pigY])

        BLUE = (10,25,225)
        BROWN = (153,76,0)
        YELLOW = (235,245,45)
        GREEN = (10,225,25)

        grass1 = 1
        grass2 = 2
        grass3 = 3
        grass4 = 4
        grass5 = 5
        dirt1 = 6
        dirt2 = 7
        dirt3 = 8
        water = 9
        sand = 10
        sand2 = 11

        TILESIZE = 256
        MAPWIDTH = 4
        MAPHEIGHT = 3

        TILESIZE2 = 16
        MAPWIDTH2 = 64
        MAPHEIGHT2 = 48

        #colors =  {
         #           grass1:g1,
          #          grass2:g2,
           #         grass3:g3,
            #        grass4:g4,
             #      dirt1:d1,
              #      dirt2:d2,
               #     dirt3:d3,
                #    water:w1,
                 #   sand:s1,
                  #  sand2:s2
                  #}
        
        tree = pygame.image.load(treeImg)
        grass = pygame.image.load(grassImg)
        dirt = pygame.image.load(dirtImg)
        water = pygame.image.load(waterImg)
        sand = pygame.image.load(sandImg)
        tree = pygame.image.load(treeImg)
        pathTrimming = pygame.image.load(PathTrimming)
        questGiver = pygame.image.load(questGiverImg)
        global scroll
        scroll = pygame.image.load(scrollImg)
        npcPrompt = pygame.image.load(npcPromptImg)
        pathTrimming1 = pygame.image.load(PathTrimming1)
        pathTrimming2 = pygame.image.load(PathTrimming2)
        pathTrimming3 = pygame.image.load(PathTrimming6)
        pathTrimming4 = pygame.image.load(PathTrimming5)
        treeStump1 = pygame.image.load(TreeStump1)
        treeStump2 = pygame.image.load(TreeStump2)
        Tree_One_Bottom_Left = pygame.image.load(TreeOneBottomLeft)
        Tree_One_Bottom_Right = pygame.image.load(TreeOneBottomRight)
        Tree_One_Top_Left = pygame.image.load(TreeOneTopLeft)
        Tree_One_Top_Right = pygame.image.load(TreeOneTopRight)
        dirtWall1 = pygame.image.load(DirtWall1)
        dirtWall2 = pygame.image.load(DirtWall2)
        dirtWall3 = pygame.image.load(DirtWall3)
        dirtWall4 = pygame.image.load(DirtWall4)
        water1 = pygame.image.load(Water1)
        water2 = pygame.image.load(Water2)
        water3 = pygame.image.load(Water3)
        water4 = pygame.image.load(Water4)
        b1 = pygame.image.load(B1)
        b2 = pygame.image.load(B2)
        b3 = pygame.image.load(B3)
        d2 = pygame.image.load(D2)
        td1 = pygame.image.load(TD1)
        td2 = pygame.image.load(TD2)
        postbox = pygame.image.load(PostBox)
        pb1 = pygame.image.load(PB1)
        pb2 = pygame.image.load(PB2)
        pb3 = pygame.image.load(PB3)
        pb4 = pygame.image.load(PB4)
        td3 = pygame.image.load(TD3)
        td4 = pygame.image.load(TD4)
        ts1 = pygame.image.load(tS1)
        ts2 = pygame.image.load(tS2)
        ts3 = pygame.image.load(tS3)
        ts4 = pygame.image.load(tS4)
        ts5 = pygame.image.load(tS5)
        ts6 = pygame.image.load(tS6)
        ts7 = pygame.image.load(tS7)
        ts8 = pygame.image.load(tS8)


        sprites = {
                    "tree":tree,
                    "g1":grass,
                    "d1":dirt,
                    "water":water,
                    "sand":sand,
                    "pT":pathTrimming,
                    "pT1":pathTrimming1,
                    "pT2":pathTrimming2,
                    "pT3":pathTrimming3,
                    "pT4":pathTrimming4,
                    "tS1":treeStump1,
                    "tS2":treeStump2,
                    "t1bl":Tree_One_Bottom_Left,
                    "t1br":Tree_One_Bottom_Right,
                    "t1tl":Tree_One_Top_Left,
                    "t1tr":Tree_One_Top_Right,
                    "dW1":dirtWall1,
                    "dW2":dirtWall2,
                    "dW3":dirtWall3,
                    "dW4":dirtWall4,
                    "w1":water1,
                    "w2":water2,
                    "w3":water3,
                    "w4":water4,
                    "b1":b1,
                    "b2":b2,
                    "b3":b3,
                    "d2":d2,
                    "td1":td1,
                    "td2":td2,
                    "pb1":pb1,
                    "pb2":pb2,
                    "pb3":pb3,
                    "pb4":pb4,
                    "td3":td3,
                    "td4":td4,
                    "ts1":ts1,
                    "ts2":ts2,
                    "ts3":ts3,
                    "ts4":ts4,
                    "ts5":ts5,
                    "ts6":ts6,
                    "ts7":ts7,
                    "ts8":ts8
                    }

        tileMap = []
        with open("C:/Users/student/Desktop/Stuff/Programming/Python/Projects/Game/tilemap.json.txt",mode = "r") as f:
            d = json.load(f)
            
        for row in d:
            tempRow = []
            for column in row:
                tempRow.append(sprites[column])
            tileMap.append(tempRow)

        gameDisplay.fill(black)
        for row in range(MAPHEIGHT2):
            for column in range(MAPWIDTH2):
                gameDisplay.blit(tileMap[row][column],[column*TILESIZE2,row*TILESIZE2])

        tileMap2 = []
        with open("C:/Users/student/Desktop/tilemap2.json.txt",mode = "r") as g:
            e = json.load(g)

        for row in e:
            tempRow2 = []
            for column in row:
                tempRow2.append(sprites[column])
            tileMap2.append(tempRow2)  

        for row in range(MAPHEIGHT2):
            for column in range(MAPWIDTH2):
                gameDisplay.blit(tileMap2[row][column],[column*TILESIZE2,row*TILESIZE2])
                
        wiz = pygame.image.load(wizImg)
        character = pygame.image.load(charImg)
        gameDisplay.blit(character,[x,y])

        if x >= 284 and y >= 136 and x <= 484 and y <= 336:
            if Quest1.questFinished == False:
              quest1Button.active = True
              quest1Button.drawButton(gameDisplay)

            if Quest1.questFinished == True:
              quest2Button.active = True
              quest2Button.drawButton(gameDisplay)
               
        if npcDirection == "left":
            npcX -= 7
            if npcX <= 320:
                npcDirection = "right"
        elif npcDirection == "right":
            npcX += 4
            if npcX >= 448:
                npcDirection = "left"
                
        if npcDirY == "up":
            npcY -= 3
            if npcY <= 172:
                npcDirY = "down"
        elif npcDirY == "down":
            npcY += 2
            if npcY >= 300:
                npcDirY = "up"
        
        gameDisplay.blit(questGiver,[npcX,300])
        
        attackPig = pygame.image.load(pigHurt)

        heart = pygame.image.load(heartImg)
        gameDisplay.blit(heart,[10,10])
        sword = pygame.image.load(swordImg)
        gameDisplay.blit(sword,[15,45])
        shield = pygame.image.load(shieldImg)
        sword2 = pygame.image.load(sword2Img)
        gameDisplay.blit(shield,[13,90])
        alt_small_pos_message_to_screen(": Health - 100",black,50,25,size = "altSmall")
        alt_small_pos_message_to_screen(": Damage - 5",black,50,70,size = "altSmall")
        alt_small_pos_message_to_screen(": Defense - 10",black,55,105,size = "altSmall")
    
        gameDisplay.blit(frontBug,[bugX,bugY])
        
       # if QuestArr1[0] == True:
        #   gameDisplay.blit(scroll,[50,50])
         #  finish_Quest1.drawButton(gameDisplay)
          # alt_small_pos_message_to_screen("Hello, I have a quest for you." ,black,100,150,size = "altSmall")
           #alt_small_pos_message_to_screen("I need you to press that button.", black,100,ui175,size = "altSmall")
           #alt_small_pos_message_to_screen("I will give you 100 gold pieces for this",black,100,200,size = "altSmall")
            
        if Quest1.showIntro == True:
           Quest1Func()

        if Quest2.showIntro == True:
           Quest2Func()

        pygame.display.update()

        #if QuestArr2[0] == True:
         #  gameDisplay.blit(scroll,[50,50])
        clock.tick(60)
        #blitChar(gameDisplay,x,y)
game_intro()
