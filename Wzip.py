import pygame, time, random


class Server(object):
    def __init__(self):
        self.spieler = {}
        self.pflanzen = {}
        self.angebote = {}

    def wachsen(self, w):
        for spieler in self.spieler.keys():
            self.spieler[spieler].wachsen(w)

    def add_spieler(self, name, gartenname="Garten"):
        self.spieler[name] = Spieler(self, gartenname)

    def add_pflanze(self, name, preis, dauer, ertrag, xp, level=1):
        if name == "Olive":
            self.pflanzen[name] = [preis, dauer, "k/Olive_k.png", ertrag, xp, level]
        else:
            self.pflanzen[name] = [preis, dauer, "k/" + name + "_k.gif", ertrag, xp, level]

    def __str__(self):
        return "Spieler: %s Spieler Pflanzen: %s Pflanzen" % (len(self.spieler), len(self.pflanzen))


class Spieler(object):
    def __init__(self, server, gartenname):
        self.geld = 100
        self.level = 1
        self.xp = 0
        self.server = server
        self.gaerten = {gartenname: Garten(self)}
        self.ftlap = ["Karotte"]
        self.wimps = []
        self.beliebt = 100
        self.inventar = {}

    def add_garten(self, gartenname):
        self.gaerten[gartenname] = Garten(self)

    def update(self):
        for item in list(self.inventar.keys()):
            if self.inventar[item] <= 0:
                del self.inventar[item]
        while self.xp >= 50 * (self.level ** 3):
            self.xp -= 50 * (self.level ** 3)
            self.level += 1
        for pflant in self.server.pflanzen.keys():
            if self.server.pflanzen[pflant][5] <= self.level and pflant not in self.ftlap:
                self.ftlap.append(pflant)

    def buy(self, pfl, x=1):
        if self.geld >= self.server.pflanzen[pfl][0]:
            if pfl not in self.inventar.keys():
                self.inventar[pfl] = 0
            self.inventar[pfl] += x
            self.geld -= self.server.pflanzen[pfl][0] * x
            self.update()

    def sell(self, pflanze, x=1):
        if pflanze in self.inventar.keys():
            self.inventar[pflanze] -= x
            self.geld += int(self.server.pflanzen[pflanze][0] * 0.75 * x)
            self.update()

    def pflanzen(self, garten, pos, pflanze):
        if self.level >= self.server.pflanzen[pflanze][5]:
            if pflanze in self.inventar.keys():
                if self.gaerten[garten].felder[pos].belegt_mit == None:
                    if pflanze in self.inventar.keys():
                        self.inventar[pflanze] -= 1
                        self.gaerten[garten].felder[pos].bebauen(pflanze)
                        self.update()

    def ernten(self, garten, pos):
        if self.gaerten[garten].felder[pos].belegt_mit != None:
            if self.gaerten[garten].felder[pos].belegt_mit.gewachsen >= 100.0:
                name = self.gaerten[garten].felder[pos].belegt_mit.name
                ertrag = self.server.pflanzen[self.gaerten[garten].felder[pos].belegt_mit.name][3]
                self.gaerten[garten].felder[pos].belegt_mit = None
                self.xp += self.server.pflanzen[name][4] * ertrag
                if name in self.inventar.keys():
                    self.inventar[name] += ertrag
                elif name not in self.inventar.keys():
                    self.inventar[name] = ertrag
                self.update()

    def blitinv(self, screen, pos, pfl):
        if pfl in self.inventar.keys():
            ima = pygame.image.load(self.server.pflanzen[pfl][2])
            ima = pygame.transform.scale(ima, (50, 50))
            screen.blit(ima, pos)
            f = pygame.font.SysFont("Arial", 15)
            screen.blit(f.render(str(self.inventar[pfl]), True, (0, 0, 0)), (pos[0] + 5, pos[1] + 35))

    def wachsen(self, w):
        for garten in self.gaerten:
            self.gaerten[garten].wachsen(w)

    def __str__(self):
        return "Geld: %s $ Gaerten: %s St�ck" % (self.geld, len(self.gaerten))


class Garten(object):
    def __init__(self, spieler):
        self.felder = {}
        self.spieler = spieler
        self.pos = (0, 0)
        for row in range(10):
            for col in range(10):
                self.felder[row, col] = Feld(self, [row, col])

    def blit(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(self.pos, (500, 500)))
        for feld in self.felder.keys():
            self.felder[feld].blit(screen)

    def wachsen(self, w):
        for feld in self.felder.keys():
            self.felder[feld].wachsen(w)

    def __str__(self):
        az = 0
        for f in self.felder.keys():
            if self.felder[f].belegt_mit != None:
                az = az + 1
        return "Felder: 10*10, %s von 100 sind belegt" % az


class Feld(object):
    def __init__(self, garten, rowcol):
        self.garten = garten
        self.belegt_mit = None
        self.rowcol = rowcol
        x = self.garten.pos[0] + self.rowcol[0] * 50
        y = self.garten.pos[1] + self.rowcol[1] * 50
        self.pos = [x, y]

    def bebauen(self, pflanze):
        self.belegt_mit = Pflanze(self, pflanze)

    def blit(self, screen):
        if self.belegt_mit == None:
            ima = pygame.transform.scale(pygame.image.load("k/entry.png"), (50, 50))
            screen.blit(ima, self.pos)
        else:
            bildname = self.garten.spieler.server.pflanzen[self.belegt_mit.name][2]
            screen.blit(pygame.transform.scale(pygame.image.load(bildname), (50, 50)), self.pos)
            if self.belegt_mit.gewachsen <= 100:
                f = pygame.font.SysFont("Arial", 20)
                screen.blit(f.render(str(int(self.belegt_mit.gewachsen)), True, (0, 0, 0)), (self.pos[0] + 5, self.pos[1] + 5))
        if self.garten.spieler.server.selected_field == self.rowcol:
            pygame.draw.rect(screen, (0, 190, 0), pygame.Rect(self.pos, (49, 49)), 2)

    def wachsen(self, w):
        if self.belegt_mit != None:
            self.belegt_mit.wachsen(w)

    def __str__(self):
        b = self.belegt_mit
        if b == None:
            b = "Nicht"
        return "Belegt: %s" % b


class Pflanze(object):
    def __init__(self, feld, name):
        self.feld = feld
        self.start_time = time.time()
        self.gewachsen = 0
        self.name = name

    def wachsen(self, w):
        if self.gewachsen < 101.0:
            time_passed = (time.time() - self.start_time) / 60.0
            self.gewachsen = time_passed / float(self.feld.garten.spieler.server.pflanzen[self.name][1]) * w

    def __str__(self):
        return "Typ: %s" % self.name


class Wimp(object):
    def __init__(self, server, spieler):
        self.start_time = time.time()
        self.nett = random.randint(1, 300) / 100.0
        self.zeit = random.randint(200 * int(self.nett), 500 * int(self.nett))
        self.einkaufsliste = {}
        self.pos = [len(spieler.wimps) * 40, 600]
        self.bild = "Wimps/Wimp" + str(random.randint(1, 5)) + ".png"
        for i in range(random.randint(1, 5)):
            pfla = random.choice(spieler.ftlap)
            self.einkaufsliste[pfla] = random.randint(50, 150) / server.pflanzen[pfla][5]

    # def go(self,spieler):
    # spieler.beliebt-=self.nett
    def blit(self, screen):
        screen.blit(pygame.image.load(self.bild), self.pos)
