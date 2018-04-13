import pygame
import sys
import random
import RPi.GPIO as GPIO
import time
from pygame.locals import *


breedte = 32
hoogte = 32
lengte = 1
grootte = 20

resolutie = breedte*grootte, hoogte*grootte

#pygame.display.set_mode(resolutie, pygame.FULLSCREEN) 

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)

pygame.init()

DISPLAY = pygame.display.set_mode(resolutie)
GROEN = (0, 255, 0)
ROOD = (255, 0, 0)
ZWART = (0,0,0)
WIT = (255, 255, 255)
GRIJS = (20, 51, 51)
eetgeluid = pygame.mixer.Sound('eet.wav')
slang = [[int(breedte/2), int(hoogte/2)]]
richting = random.randrange(1,4)
score = 0

def teken():
    pygame.draw.rect(DISPLAY, GROEN, (0, 0, grootte*breedte-1, grootte*hoogte-1))
    pygame.draw.rect(DISPLAY, ZWART, (1, 1, grootte*breedte-3, grootte*hoogte-3))

    for s in slang:
        pygame.draw.rect(DISPLAY, WIT, (s[0]*grootte, s[1]*grootte, grootte, grootte))
    
    pygame.draw.rect(DISPLAY, ROOD, (fruit[0]*grootte, fruit[1]*grootte, grootte, grootte))

    for w in range(breedte-1):
        pygame.draw.line(DISPLAY, GRIJS, ((w+1)*grootte, 1), ((w+1)*grootte, hoogte*grootte-2), 1)       
    for h in range(hoogte-1):
        pygame.draw.line(DISPLAY, GRIJS, (1, (h+1)*grootte), (breedte*grootte-2, (h+1)*grootte), 1)       

    pygame.display.update()

fruit = [random.randrange(1,breedte-1), random.randrange(1,hoogte-1)]

while True:
    for e in pygame.event.get():
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            k = pygame.key.get_pressed()
            if k[K_UP] and richting != 3: 
                richting = 1
            if k[K_RIGHT] and richting != 4: 
                richting = 2
            if k[K_DOWN] and richting != 1: 
                richting = 3
            if k[K_LEFT] and richting != 2: 
                richting = 4

    oude_slang = list(slang)
    slang = []
    slang.append(list(oude_slang[0]))

    if richting == 1:
        slang[0][1] = slang[0][1]-1
    if richting == 2:
        slang[0][0] = slang[0][0]+1
    if richting == 3:
        slang[0][1] = slang[0][1]+1
    if richting == 4:
        slang[0][0] = slang[0][0]-1

    if slang[0][1] < 0: 
        slang[0][1] = hoogte-1
    if slang[0][0] > breedte-1: 
        slang[0][0] = 0
    if slang[0][1] > hoogte-1: 
        slang[0][1] = 0
    if slang[0][0] < 0: 
        slang[0][0] = breedte-1

    if slang[0] == fruit:
        eetgeluid.play()
        fruit = [random.randrange(1, breedte-1), random.randrange(1, hoogte-1)]
        lengte = lengte + 1
        score = score + 1
        GPIO.output(18,GPIO.HIGH)
        GPIO.output(18,GPIO.LOW)


    for t in range(lengte-1):
        slang.append(list(oude_slang[t]))

    teken()

    pygame.time.delay(240-int(lengte/5)*20)
