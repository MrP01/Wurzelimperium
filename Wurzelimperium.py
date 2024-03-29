import logging

import pygame

from defs import *
from superclass import *
from Wzip import *

pygame.init()
size = width, height = 1000, 800
screen = pygame.display.set_mode(size)
f = pygame.font.SysFont("Arial", 20)
f2 = pygame.font.SysFont("Arial", 21)
logging.basicConfig(level=logging.DEBUG)

try:
    stick = pygame.joystick.Joystick(0)
    stick.init()
    # print(stick.get_numaxes())
except pygame.error:
    print("No joystick found, it will be pretty boring then")
    stick = None

CHEATS = True  # True = An; False = Aus
WACHSTUM = 1000  # 100=Echtzeit; 1000=10*so schnell

clock = pygame.time.Clock()

server, success = load(Server())
if not success:
    logging.info("Generating new")
    neu(server)
cpn = "Peter"
cgn = "Garden"
cp = server.spieler[cpn]
cp.wimps.append(Wimp(server, cp))
cg = cp.gaerten[cgn]
pfl = "Karotte"
server.selected_field = [0, 0]
cheat4 = False
cheat6 = "pflanzen"
server.wachsen(WACHSTUM)
sell = Superclass((900, 30), "img/Buttons/Sell.jpg")
kaufen = Superclass((900, 60), "img/Buttons/Kaufen.jpg")
nexpla = Superclass((0, 755), "img/Buttons/Next2.jpg")
nexgar = Superclass((0, 779), "img/Buttons/Next2.jpg")
timi = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save(server)
            exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            save(server)
            exit()
        if event.type == pygame.KEYDOWN:
            cp.update()
            if CHEATS:
                if event.key == 282:
                    print("Cheat Pflanze")
                    if pfl in cp.inventar.keys():
                        cp.inventar[pfl] += 1
                    else:
                        cp.inventar[pfl] = 1
                if event.key == 283:
                    print("Cheat Geld")
                    cp.geld += 500
                if event.key == 284:
                    print("Cheat Level")
                    cp.level += 1
                    cp.update()
                if event.key == 285:
                    print("Cheat Xp")
                    cp.xp += 1000
                    cp.update()
                if event.key == 286:
                    if cheat4:
                        cheat4 = False
                        print("Cheat Fertig aus")
                    else:
                        print("Cheat Fertig an")
                    cheat4 = True
            if event.key == 287:
                print("Wachstums-Beschleunigung")
                WACHSTUM += 50
            if event.key == 288:
                print("Garten anbauen")
                if cheat6 == "pflanzen":
                    for feld in cg.felder.keys():
                        cp.pflanzen(cgn, feld, pfl)
                    cheat6 = "ernten"
                elif cheat6 == "ernten" and cg.felder[feld].belegt_mit is not None:
                    for feld in cg.felder.keys():
                        if cg.felder[feld].belegt_mit.gewachsen >= 100:
                            cp.ernten(cgn, feld)
                cheat6 = "pflanzen"
            cp.update()

        if event.type == pygame.JOYHATMOTION:
            server.selected_field[0] = min(9, max(0, server.selected_field[0] + event.value[0]))
            server.selected_field[1] = min(9, max(0, server.selected_field[1] - event.value[1]))

        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == 1:
                if cg.felder[server.selected_field[0], server.selected_field[1]].belegt_mit is not None:
                    if cheat4:
                        cg.felder[server.selected_field[0], server.selected_field[1]].belegt_mit.gewachsen = 100
                    if cg.felder[server.selected_field[0], server.selected_field[1]].belegt_mit.gewachsen >= 100:
                        cp.ernten(cgn, tuple(server.selected_field))
                else:
                    cp.pflanzen(cgn, tuple(server.selected_field), pfl)
                if not stick.get_button(0):
                    if event.button == 3:
                        cp.sell(pfl)
                    if event.button == 2:
                        cp.buy(pfl)
            else:
                if event.button == 3:
                    if pfl in cp.inventar:
                        cp.sell(pfl, cp.inventar[pfl])
                if event.button == 2:
                    cp.buy(pfl, cp.geld // server.pflanzen[pfl][0])
                if event.button == 5:
                    pfl = nexter(cp.ftlap, pfl)
                if event.button == 4:
                    pfl = beforer(cp.ftlap, pfl)

        if event.type == pygame.MOUSEBUTTONDOWN:
            mp = pygame.mouse.get_pos()
            if event.button == 1:
                if onfield(mp, cg.pos, (500, 500)):
                    xx = (mp[0] - cg.pos[0]) // 50
                    yy = (mp[1] - cg.pos[1]) // 50
                    if cheat4 and cg.felder[xx, yy].belegt_mit is not None:
                        cg.felder[xx, yy].belegt_mit.gewachsen = 100
                    else:
                        cp.pflanzen(cgn, (xx, yy), pfl)
                if onfield(mp, (900, 30), (100, 30)):
                    cp.sell(pfl)
                if onfield(mp, (900, 60), (100, 30)):
                    cp.buy(pfl)
                if onfield(mp, cg.pos, (500, 500)):
                    xx = (mp[0] - cg.pos[0]) // 50
                    yy = (mp[1] - cg.pos[1]) // 50
                    cp.ernten(cgn, (xx, yy))
                if onfield(mp, (0, 755), (28, 21)):
                    cpn = nexter(list(server.spieler.keys()), cpn)
                    cp = server.spieler[cpn]
                    cgn = list(cp.gaerten.keys())[0]
                    cg = cp.gaerten[cgn]
                    pfl = "Karotte"
                if onfield(mp, (0, 779), (28, 21)):
                    cgn = nexter(list(cp.gaerten.keys()), cgn)
                    cg = cp.gaerten[cgn]
            if event.button == 3:
                if onfield(mp, (900, 30), (100, 30)):
                    cp.sell(pfl, cp.inventar[pfl])
                if onfield(mp, (900, 60), (100, 30)):
                    cp.buy(pfl, cp.geld // server.pflanzen[pfl][0])
            if event.button == 4:
                pfl = nexter(cp.ftlap, pfl)
            if event.button == 5:
                pfl = beforer(cp.ftlap, pfl)

    time_passed = clock.tick(12)
    timi += time_passed
    # if timi >= 10000:
    # if random.randint(1,100000) <= cp.beliebt:
    screen.fill([0, 150, 0])
    cg.wachsen(WACHSTUM)
    screen.blit(f.render(pfl + " : " + str(server.pflanzen[pfl][0]) + " $", True, (0, 0, 0)), (500, 0))
    screen.blit(f.render("Wachstum : " + str(server.pflanzen[pfl][1]) + " min", True, (0, 0, 0)), (500, 22))
    screen.blit(f.render("Ertrag : " + str(server.pflanzen[pfl][3]), True, (0, 0, 0)), (500, 44))
    screen.blit(f.render("Erfordertes Level : " + str(server.pflanzen[pfl][5]), True, (0, 0, 0)), (500, 66))
    screen.blit(f.render("Level : " + str(cp.level), True, (0, 0, 0)), (500, 779))
    screen.blit(f.render("Xp : " + str(cp.xp), True, (0, 0, 0)), (600, 779))
    screen.blit(f.render("Xp noch : " + str(50 * ((cp.level) ** 2) - cp.xp), True, (0, 0, 0)), (800, 779))
    screen.blit(f.render(str(cp.geld) + " $", True, (0, 0, 0)), (900, 0))
    screen.blit(f2.render(cpn, True, (0, 0, 0)), (30, 755))
    screen.blit(f2.render(cgn, True, (0, 0, 0)), (30, 779))
    screen.blit(f.render("Gibt Xp : " + str(server.pflanzen[pfl][4]), True, (0, 0, 0)), (500, 88))
    screen.blit(pygame.transform.scale(pygame.image.load(server.pflanzen[pfl][2]), (50, 50)), (510, 110))
    if pfl in cp.inventar.keys():
        sell.blit(screen)
    if cp.geld >= server.pflanzen[pfl][0] and cp.level >= server.pflanzen[pfl][5]:
        kaufen.blit(screen)
    for wimp in cp.wimps:
        wimp.blit(screen)
    nexgar.blit(screen)
    nexpla.blit(screen)
    cg.blit(screen)
    cp.blitinv(screen, (700, 0), pfl)
    pygame.display.flip()
    # pygame.display.update()
