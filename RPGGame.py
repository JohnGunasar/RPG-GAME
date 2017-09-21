import pygame
import time
import random

pygame.init()

display_width = 1024
display_height = 768

backgroundImg = 'C:/Users/student/Desktop/BackGround.jpg'

gameDisplay = pygame.display.set_mode((display_width,display_height))

pygame.display.set_caption('Game Name')
pygame.display.update()

white = (255,255,255)
black = (0,0,0)
red = (255,20,25)
green = (34,177,76)
titleColor = (102,153,217)
clock = pygame.time.Clock()

smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("Algerian", 50)
largefont = pygame.font.SysFont("Algerian", 85)

smallBlackadderITC = pygame.font.SysFont("Blackadder ITC",25)
medBlackadderITC = pygame.font.SysFont("BlackadderITC",50)
largeBlackadderITC = pygame.font.SysFont("Blackadder ITC",85)

def text_objects(text, color,size = "small"):

    if size == "small":
        textSurface = smallfont.render(text, True, color)
    if size == "medium":
        textSurface = medfont.render(text, True, color)
    if size == "large":
        textSurface = largefont.render(text, True, color)

    return textSurface, textSurface.get_rect()
   
def message_to_screen(msg,color, y_displace = 0, size = "small"):
    textSurf, textRect = text_objects(msg,color,size)
    textRect.center = (int(display_width / 2), int(display_height / 2)+y_displace)
    gameDisplay.blit(textSurf, textRect)

def alt_message_to_screen (msg,color,x,y,size = "small"):
    textSurf,textRect = text_objects(msg,color,size)
    gameDisplay.blit(textSurf,textRect)

def pause():

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


def characterCreation():

    charCreate = True

    while charCreate:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(white)
        message_to_screen("This is a test text",green,-100,size = "large")
        pygame.display.update()

def game_intro():

    intro = True

    while intro:
        for event in pygame.event.get():
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
                        print(event)
                        characterCreation()
                        intro = False
                        
        backImg = pygame.image.load(backgroundImg)
        gameDisplay.blit(backImg,[0,0])
        message_to_screen("<Game Name>",green,-100,size="large")
        message_to_screen("To create your character press C",red,size = "medium")
        #message_to_screen("To quit, press Q",red,0,size = "medium")
        pygame.display.update()
        clock.tick(15)

game_intro()

def gameLoop():
    gameExit = False
    gameOver = False
    FPS = 15
    
    while not gameExit:
        
        if gameOver == True:
            #gameDisplay.fill(white)
            message_to_screen("Game Over",red,-50,size="large")
            message_to_screen("Press C to play again or Q to exit",black,50)
            pygame.display.update()
            while gameOver == True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        gameExit = True
                        gameOver = False

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_c:
                            gameLoop()
                        elif event.key == pygame.K_q:
                            
                            gameExit = True
                            gameOver = False
         


        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                gameExit = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    pass
                    
                elif event.key == pygame.K_RIGHT:
                    pass
                    
                elif event.key == pygame.K_UP:
                    pass
                    
                    
                elif event.key == pygame.K_DOWN:
                    pass

                elif event.key == pygame.K_p:
                    pause()         

        gameDisplay.fill(white)
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    quit()


gameLoop()
