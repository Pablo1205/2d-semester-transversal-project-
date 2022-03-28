import pygame, sys
from paf_11 import *
mainClock = pygame.time.Clock()
from pygame.locals import *
from pygame_functions import *
pygame.init()
pygame.display.set_caption('Paf le Nain')
screen = pygame.display.set_mode((1920, 1080),0,32)
#here are all the variables used in the code, being the sprites of the background and the chariot and some basic fonts sizes
background = pygame.image.load('Fond.jpg')
chariot = pygame.image.load('chariot_menu.png')
font = pygame.font.SysFont(None, 20)
font_big = pygame.font.SysFont(None, 75)
font_huge = pygame.font.SysFont(None, 95)
font_medium = pygame.font.SysFont(None, 55)
sound = 1

def draw_text(text, font, color, surface, x, y): #this function creates a text, we used it a lot later so this is just a basic way to display text
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

click = False
highscore=get_highscore()
highscore="Highscore : "+str(highscore)

def main_menu():
    frames=0 
    chariotx=0
    charioty=545 #(0,545) is the starting position of you chariot
    has_jumped=False
    while True:
        chariotx+=2 #every loop, the chariot will go 2 pixels to the right
        if chariotx>1800: #in order to get the cariot to loop around the window, when it reaches the left (1920 pixel - the chariot pixel width), we reset its position to the right
            chariotx=0
        if has_jumped==False: #this is the initialisation of a quick animation that cannot reproduce itself if it already is occuring
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key==pygame.K_SPACE: #in order to trigger the animation, you need to press space
                        has_jumped=True
        if has_jumped==True: #we based the animation on the clock, to have a quick animation, half of the animation is on 30 frames
            if frames<30: #the 30 first frames make the chariot go upwards
                chariotx+=2
                charioty-=2
                frames+=1
            else :
                if frames<60: #once we've reach 30 frames, the chariot needs to come back down on the tracks
                    chariotx+=2
                    charioty+=2
                    frames+=1
                else: #when the animation is finished, we reset all the initial variables
                    frames=0
                    has_jumped=False
        screen.blit(background,(0,0))
        screen.blit(chariot,(chariotx,charioty)) 
        mx, my = pygame.mouse.get_pos()
        button_1 = pygame.Rect(800, 500, 200, 50) #in the menu we have 2 buttons
        button_2 = pygame.Rect(800, 600, 200, 50)
        if button_1.collidepoint((mx, my)): #this loop is used to make an animation on the text, when you hoover on the text, the font is bigger than usual
            draw_text('Play', font_huge, (150, 130, 125), screen, 800, 500) 
            if click: #click is a variable that is true only if you press mousebutton1, meaning here that if you click, you launch the game loop
                game()
                main_menu()
        else:
            draw_text('Play', font_big, (150, 130, 125), screen, 800, 500)
        if button_2.collidepoint((mx, my)): #same as before but with the options
            draw_text('Options', font_huge, (150, 130, 125), screen, 800, 600)
            if click:
                options(sound)
        else:
            draw_text('Options', font_big, (150, 130, 125), screen, 800, 600)
        draw_text(highscore, font_big, (0, 0, 0), screen, 20, 20)
        pygame.display.flip()
        
        click = False
        for event in pygame.event.get(): #we have here a loop that enable to quit the game and to get the information on the click
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        pygame.display.update()
        mainClock.tick(60)
 
def options(sound): #when you click option, this function starts. It is mostly just displaying
    running = True
    while running:
        mx, my = pygame.mouse.get_pos()
        background = pygame.image.load('Background_Options.png')
        left_arrow = pygame.image.load('Left arrow.png')
        right_arrow = pygame.image.load('Right arrow.png')
        spacebar = pygame.image.load('Space bar.png')
        screen.blit(background,(0,0))
        screen.blit(left_arrow,(530,415))
        screen.blit(right_arrow,(530,615))
        screen.blit(spacebar,(530,815))
        pygame.display.flip()
        draw_text('Options', font_big, (255, 255, 255), screen, 20, 20)
        draw_text('Sound', font_big, (255, 255, 255), screen, 300, 260)
        draw_text('Rules', font_big, (255, 255, 255), screen, 520, 350)
        draw_text('Press                 to go LEFT', font_medium, (255, 255, 255), screen, 390, 455) #we have some space in between the words to let space for some pictures
        draw_text('Press                 to go RIGHT', font_medium, (255, 255, 255), screen, 390, 655)
        draw_text('Press                                             to go JUMP', font_medium, (255, 255, 255), screen, 390, 855)
        sound_1 = pygame.Rect(540, 250, 50, 50)
        sound_2 = pygame.Rect(615, 250, 50, 50)
        sound_3 = pygame.Rect(690, 250, 50, 50)
        sound_4 = pygame.Rect(765, 250, 50, 50)
        sound_button_color=(150, 130, 125)
        sound_used_button_color=(180, 10, 10)
        if sound==1: #we use the variable sound to change the sound of the game, depending on the volume you chose, the button lights up red or grey/brown
            pygame.draw.rect(screen, sound_used_button_color, sound_1)
            pygame.draw.rect(screen, sound_button_color, sound_2)
            pygame.draw.rect(screen, sound_button_color, sound_3)
            pygame.draw.rect(screen, sound_button_color, sound_4)
        if sound==2:   
            pygame.draw.rect(screen, sound_button_color, sound_1)
            pygame.draw.rect(screen, sound_used_button_color, sound_2)
            pygame.draw.rect(screen, sound_button_color, sound_3)
            pygame.draw.rect(screen, sound_button_color, sound_4)
        if sound==3:
            pygame.draw.rect(screen, sound_button_color, sound_1)
            pygame.draw.rect(screen, sound_button_color, sound_2)
            pygame.draw.rect(screen, sound_used_button_color, sound_3)
            pygame.draw.rect(screen, sound_button_color, sound_4)
        if sound==4:
            pygame.draw.rect(screen, sound_button_color, sound_1)
            pygame.draw.rect(screen, sound_button_color, sound_2)
            pygame.draw.rect(screen, sound_button_color, sound_3)
            pygame.draw.rect(screen, sound_used_button_color, sound_4)
        pygame.display.update()
        click = False
        for event in pygame.event.get(): #loop to quit the option and come back to the main loop with the menu
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    return sound
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        if sound_1.collidepoint((mx, my)): #these check if the user is on the button and changes the sound value depending on where he clicks
            if click:
                sound=1
        if sound_2.collidepoint((mx, my)):
            if click:
                sound=2
        if sound_3.collidepoint((mx, my)):
            if click:
                sound=3
        if sound_4.collidepoint((mx, my)):
            if click:
                sound=4
        mainClock.tick(60)
main_menu()