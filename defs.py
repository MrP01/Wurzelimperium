import pickle


def neu(s):
    s.add_pflanze("Karotte", 6, 10, 2, 1, 1)
    s.add_pflanze("Salat", 8, 14, 2, 1, 2)
    s.add_pflanze("Gurke", 14, 40, 4, 4, 3)
    s.add_pflanze("Radieschen", 22, 50, 3, 5, 4)
    s.add_pflanze("Erdbeere", 44, 120, 4, 12, 5)
    s.add_pflanze("Tomate", 50, 140, 4, 14, 6)
    s.add_pflanze("Zwiebel", 176, 480, 4, 48, 7)
    s.add_pflanze("Spinat", 210, 560, 4, 56, 8)
    s.add_pflanze("Ringelblume", 180, 360, 4, 36, 9)
    s.add_pflanze("Blumenkohl", 378, 1000, 4, 100, 10)
    s.add_pflanze("Kartoffel", 360, 960, 4, 96, 11)
    s.add_pflanze("Knoblauch", 510, 1320, 4, 132, 12)
    s.add_pflanze("Brokkoli", 448, 1200, 4, 120, 13)
    s.add_pflanze("Paprika", 732, 2400, 5, 240, 14)
    s.add_pflanze("Sonnenblume", 150, 300, 3, 30, 15)
    s.add_pflanze("Spargel", 780, 2520, 5, 504, 16)
    s.add_pflanze("Aubergine", 888, 2880, 5, 288, 17)
    s.add_pflanze("Zucchini", 1104, 2880, 4, 288, 18)
    s.add_pflanze("Heidelbeere", 504, 1920, 6, 192, 19)
    s.add_pflanze("Himbeere", 760, 2880, 5, 288, 20)
    s.add_pflanze("Johannisbeere", 575, 2160, 6, 216, 21)
    s.add_pflanze("Brombeere", 3000, 2880, 3, 288, 22)
    s.add_pflanze("Rose", 350, 420, 2, 42, 23)
    s.add_pflanze("Mirabelle", 5628, 8640, 10, 3456, 24)
    s.add_pflanze("Apfel", 3096, 5760, 12, 2304, 25)
    s.add_pflanze("Kuerbis", 2280, 8640, 6, 864, 26)
    s.add_pflanze("Birne", 4680, 7200, 10, 2880, 27)
    s.add_pflanze("Kirsche", 4140, 11520, 18, 4608, 28)
    s.add_pflanze("Pflaume", 6240, 14400, 15, 5760, 29)
    s.add_pflanze("Trauben", 2210, 720, 2, 144, 30)
    s.add_pflanze("Walnuss", 6840, 20160, 19, 8064, 31)
    s.add_pflanze("Basilikum", 895, 1080, 3, 216, 32)
    s.add_pflanze("Champignon", 3249, 2880, 5, 576, 33)
    s.add_pflanze("Olive", 7800, 14400, 18, 5760, 34)
    s.add_pflanze("Tulpe", 400, 1200, 5, 120, 35)
    s.add_pflanze("Rotkohl", 1800, 4320, 6, 432, 36)
    s.add_pflanze("Gerbera", 300, 560, 4, 56, 37)
    s.add_pflanze("Lavendel", 6660, 7200, 8, 1440, 38)
    s.add_spieler("Peter", "Garden")
    s.add_spieler("Gartenzwerg Konrad", "Extrem Garten")
    s.add_spieler("Joerg", "Das Karee")
    s.add_spieler("Lotti", "Gemuesegarten")
    s.add_spieler("Ute", "Blumenbeet")


def save(obj, filename="Data.txt"):
    with open(filename, "wb") as f:
        pickle.dump(obj, f)


def load(fallback, filename="Data.txt"):
    try:
        with open(filename, "rb") as f:
            return (pickle.load(f), True)
    except pickle.PickleError:
        return (fallback, False)


def onfield(posof, pos, size):
    if pos[0] < posof[0] < pos[0] + size[0]:
        if pos[1] < posof[1] < pos[1] + size[1]:
            return True


def nexter(list, object):
    list.sort()
    ind = list.index(object)
    if ind == len(list) - 1:
        return list[0]
    else:
        return list[ind + 1]


def beforer(list, object):
    list.sort()
    ind = list.index(object)
    if ind == 0:
        return list[len(list) - 1]
    else:
        return list[ind - 1]
