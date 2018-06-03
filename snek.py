# Alles wat de game nodig heeft
import pygame
import sys
import random
import time
from pygame.locals import *

#Om de pygame te starten
pygame.init()
pygame.font.init()

# De afmetingen 
BREEDTE = 32
HOOGTE = 32
GROOTTE = 20
RESOLUTIE = BREEDTE*GROOTTE, HOOGTE*GROOTTE
# Scherm maken 
DISPLAY = pygame.display.set_mode(RESOLUTIE)


# Verschillende lettergroottes
STATUS = pygame.font.SysFont('Arial', GROOTTE)
GROOT = pygame.font.SysFont('Arial Bold', GROOTTE*3)

# De kleuren
GROEN = (0, 255, 0)
ROOD = (255, 0, 0)
ZWART = (0,0,0)
WIT = (255, 255, 255)
GRIJS = (20, 51, 51)
PAARS = (144, 0, 144)

# richtingen
BOVEN = 1
RECHTS = 2
ONDER = 3
LINKS = 4

EETGELUID = pygame.mixer.Sound('eet.wav')

# slang 1 blokje midden veld
slang = [[int(BREEDTE/2), int(HOOGTE/2)]]
lengte = 1
score = 0
GAMEOVER = False

# richting start slang 
richting = random.randrange(1,4)

# snelheid slang begin 
FPS = 5
KLOK = pygame.time.Clock()

# fruit op random plaats
fruit = [random.randrange(1,BREEDTE-1), random.randrange(1,HOOGTE-1)]

# functie alles tekenen op het scherm
def teken():
    # een groen kader
    pygame.draw.rect(DISPLAY, GROEN, (0, 0, GROOTTE*BREEDTE-1, GROOTTE*HOOGTE-1))
    pygame.draw.rect(DISPLAY, ZWART, (1, 1, GROOTTE*BREEDTE-3, GROOTTE*HOOGTE-3))

    # elk bloje slang teken in het wit
    for s in slang:
        pygame.draw.rect(DISPLAY, WIT, (s[0]*GROOTTE, s[1]*GROOTTE, GROOTTE, GROOTTE))
    
    # teken fruit in het rood 
    pygame.draw.rect(DISPLAY, ROOD, (fruit[0]*GROOTTE, fruit[1]*GROOTTE, GROOTTE, GROOTTE))

    # teken lijntjes
    for w in range(BREEDTE-1):
        pygame.draw.line(DISPLAY, GRIJS, ((w+1)*GROOTTE, 1), ((w+1)*GROOTTE, HOOGTE*GROOTTE-3), 1)       
    for h in range(HOOGTE-1):
        pygame.draw.line(DISPLAY, GRIJS, (1, (h+1)*GROOTTE), (BREEDTE*GROOTTE-3, (h+1)*GROOTTE), 1)  

    # tekst op display teken
    scoretekst = STATUS.render('Score: '+str(score), False, PAARS)
    fpstekst = STATUS.render('Snelheid: '+str(FPS), False, PAARS)
    DISPLAY.blit(scoretekst,(GROOTTE,GROOTTE/2))
    DISPLAY.blit(fpstekst,(GROOTTE,GROOTTE*2))

    # tonen wat we getekend hebben
    pygame.display.update()




# zolang niet game over...
while GAMEOVER == False:

    # verwerk events van pygame
    for e in pygame.event.get():
        # als toets gedrukt...
        if e.type == KEYDOWN:
            # als escape: stop spel
            if e.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            # anders: verander richting afhankelijk
            # op welk pijltje gedrukt wordt
            k = pygame.key.get_pressed()
            if k[K_UP] and richting != ONDER: 
                richting = BOVEN
            if k[K_RIGHT] and richting != LINKS: 
                richting = RECHTS
            if k[K_DOWN] and richting != BOVEN: 
                richting = ONDER
            if k[K_LEFT] and richting != RECHTS: 
                richting = LINKS

    # eerst slang kopieren naar oude slang
    oude_slang = list(slang)

    # nieuwe slang maken en de kop van de oude slang erin steken
    slang = []
    slang.append(list(oude_slang[0]))


    # Kopje van de slang verplaatsen naar de richting 
    # van de toets
    if richting == BOVEN:
        slang[0][1] = slang[0][1]-1
    if richting == RECHTS:
        slang[0][0] = slang[0][0]+1
    if richting == ONDER:
        slang[0][1] = slang[0][1]+1
    if richting == LINKS:
        slang[0][0] = slang[0][0]-1

    #als slang uit het veld gaat komt hij er aan de 
    # andere kant weer in 
    if slang[0][1] < 0: 
        slang[0][1] = HOOGTE-1
    if slang[0][0] > BREEDTE-1: 
        slang[0][0] = 0
    if slang[0][1] > HOOGTE-1: 
        slang[0][1] = 0
    if slang[0][0] < 0: 
        slang[0][0] = BREEDTE-1

    # als het kopje van de oude slang het lijfje raakt 
    # dan is het game over
    if slang[0] in oude_slang:
        GAMEOVER = True

    # als het kopje van de slang op het fruit zit
    if slang[0] == fruit:
        EETGELUID.play()
        fruit = [random.randrange(1, BREEDTE-1), random.randrange(1, HOOGTE-1)]
        lengte = lengte + 1
        score = score + 1
        FPS = min(5 + int(score/5), 25)

    # voeg oude slang toe aan nieuwe slang :
    # als fruit gegeten: heel de oude slang toevoegen
    # als geen fruit gegeten: alles behalve het laatste blokje
    for t in range(lengte-1):
        slang.append(list(oude_slang[t]))

    # alles tekenen
    teken()

    # zorgt ervoor dat slang niet oneindig snel gaat
    KLOK.tick(FPS)


# game over tekst + score tonen op display
gameovertekst = GROOT.render('GAME OVER', False, ROOD)
scoretekst = STATUS.render('Score: '+str(score), False, ROOD)
DISPLAY.blit(gameovertekst,(BREEDTE*GROOTTE/2-gameovertekst.get_width()/2,HOOGTE*GROOTTE/2-GROOTTE))
DISPLAY.blit(scoretekst,(BREEDTE*GROOTTE/2-scoretekst.get_width()/2,HOOGTE*GROOTTE/2+GROOTTE))
pygame.display.update()

# blijft wachten tot je op esc drukt
while True:
    for e in pygame.event.get():
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
