import pygame
import sys
import random
from pygame.locals import *

breedte = 32
hoogte = 32
lengte = 1
resolutie = breedte*10, hoogte*10

# pygame.display.set_mode(resolutie, pygame.FULLSCREEN) 

pygame.init()

DISPLAY = pygame.display.set_mode(resolutie, pygame.FULLSCREEN )
GROEN = (0, 255, 0)
ROOD = (255, 0, 0)
ZWART = (0, 0, 0)
WIT = (255, 255, 255)
eetgeluid = pygame.mixer.Sound('eet.wav')

slang = [[int(breedte/2), int(hoogte/2)]]
richting = random.randrange(1,4)

def teken():
    pygame.draw.rect(DISPLAY, GROEN, (0, 0, 10*breedte-1, 10*hoogte-1))
    pygame.draw.rect(DISPLAY, ZWART, (1, 1, 10*breedte-3, 10*hoogte-3))
    
    for s in slang:
        pygame.draw.rect(DISPLAY, WIT, (s[0]*10, s[1]*10, 9, 9))
    
    pygame.draw.rect(DISPLAY, ROOD, (fruit[0]*10, fruit[1]*10, 9, 9))

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
    if slang[0][0] < 0: slang[0][0] = 
        breedte-1

    if slang[0] == fruit:
        eetgeluid.play()
        fruit = [random.randrange(1, breedte-1), random.randrange(1, hoogte-1)]
        lengte = lengte + 1

    for t in range(lengte-1):
        slang.append(list(oude_slang[t]))

    teken()

    pygame.time.delay(240-int(lengte/5)*20)
