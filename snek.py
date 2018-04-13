import pygame
import sys
import random
import RPi.GPIO as GPIO
import time
from pygame.locals import *


BREEDTE = 32
HOOGTE = 32
GROOTTE = 20
RESOLUTIE = BREEDTE*GROOTTE, HOOGTE*GROOTTE

#pygame.display.set_mode(resolutie, pygame.FULLSCREEN) 

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)

pygame.init()
pygame.font.init()

STATUS = pygame.font.SysFont('Arial', GROOTTE)
GROOT = pygame.font.SysFont('Arial Bold', GROOTTE*3)

DISPLAY = pygame.display.set_mode(RESOLUTIE)
GROEN = (0, 255, 0)
ROOD = (255, 0, 0)
ZWART = (0,0,0)
WIT = (255, 255, 255)
GRIJS = (20, 51, 51)
PAARS = (144, 0, 144)
BOVEN = 1
RECHTS = 2
ONDER = 3
LINKS = 4
EETGELUID = pygame.mixer.Sound('eet.wav')
slang = [[int(BREEDTE/2), int(HOOGTE/2)]]
richting = random.randrange(1,4)
score = 0
lengte = 1
FPS = 5
KLOK = pygame.time.Clock()
GAMEOVER = False

def teken():
    pygame.draw.rect(DISPLAY, GROEN, (0, 0, GROOTTE*BREEDTE-1, GROOTTE*HOOGTE-1))
    pygame.draw.rect(DISPLAY, ZWART, (1, 1, GROOTTE*BREEDTE-3, GROOTTE*HOOGTE-3))

    for s in slang:
        pygame.draw.rect(DISPLAY, WIT, (s[0]*GROOTTE, s[1]*GROOTTE, GROOTTE, GROOTTE))
    
    pygame.draw.rect(DISPLAY, ROOD, (fruit[0]*GROOTTE, fruit[1]*GROOTTE, GROOTTE, GROOTTE))

    for w in range(BREEDTE-1):
        pygame.draw.line(DISPLAY, GRIJS, ((w+1)*GROOTTE, 1), ((w+1)*GROOTTE, HOOGTE*GROOTTE-3), 1)       
    for h in range(HOOGTE-1):
        pygame.draw.line(DISPLAY, GRIJS, (1, (h+1)*GROOTTE), (BREEDTE*GROOTTE-3, (h+1)*GROOTTE), 1)  

    scoretekst = STATUS.render('Score: '+str(score), False, PAARS)
    fpstekst = STATUS.render('Snelheid: '+str(FPS), False, PAARS)

    DISPLAY.blit(scoretekst,(GROOTTE,GROOTTE/2))
    DISPLAY.blit(fpstekst,(GROOTTE,GROOTTE*2))

    pygame.display.update()

fruit = [random.randrange(1,BREEDTE-1), random.randrange(1,HOOGTE-1)]

while GAMEOVER == False:
    GPIO.output(18,GPIO.LOW)
    for e in pygame.event.get():
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            k = pygame.key.get_pressed()
            if k[K_UP] and richting != ONDER: 
                richting = BOVEN
            if k[K_RIGHT] and richting != LINKS: 
                richting = RECHTS
            if k[K_DOWN] and richting != BOVEN: 
                richting = ONDER
            if k[K_LEFT] and richting != RECHTS: 
                richting = LINKS

    oude_slang = list(slang)
    slang = []
    slang.append(list(oude_slang[0]))

    if richting == BOVEN:
        slang[0][1] = slang[0][1]-1
    if richting == RECHTS:
        slang[0][0] = slang[0][0]+1
    if richting == ONDER:
        slang[0][1] = slang[0][1]+1
    if richting == LINKS:
        slang[0][0] = slang[0][0]-1

    if slang[0][1] < 0: 
        slang[0][1] = HOOGTE-1
    if slang[0][0] > BREEDTE-1: 
        slang[0][0] = 0
    if slang[0][1] > HOOGTE-1: 
        slang[0][1] = 0
    if slang[0][0] < 0: 
        slang[0][0] = BREEDTE-1

    if slang[0] in oude_slang:
        GAMEOVER = True

    if slang[0] == fruit:
        EETGELUID.play()
        fruit = [random.randrange(1, BREEDTE-1), random.randrange(1, HOOGTE-1)]
        lengte = lengte + 1
        score = score + 1
        GPIO.output(18,GPIO.HIGH)
        FPS = min(5 + int(score/5), 25)

    for t in range(lengte-1):
        slang.append(list(oude_slang[t]))

    teken()

    KLOK.tick(FPS)
    
gameovertekst = GROOT.render('GAME OVER', False, ROOD)
scoretekst = STATUS.render('Score: '+str(score), False, ROOD)
DISPLAY.blit(gameovertekst,(BREEDTE*GROOTTE/2-gameovertekst.get_width()/2,HOOGTE*GROOTTE/2-GROOTTE))
DISPLAY.blit(scoretekst,(BREEDTE*GROOTTE/2-scoretekst.get_width()/2,HOOGTE*GROOTTE/2+GROOTTE))
pygame.display.update()

while True:
    for e in pygame.event.get():
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
    GPIO.output(18,GPIO.HIGH)       
    time.sleep(1)
    GPIO.output(18,GPIO.LOW)