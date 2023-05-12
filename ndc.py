import pyxel
import random

"""
DOCUMENTATION GOES HERE
"""

MIN_OBJECTS_PER_SCREEN = 100
MAX_OBJECTS_PER_SCREEN = 140
PLAYER_SPEED = 2

UPKEYS = [pyxel.KEY_W,pyxel.KEY_UP]
DOWNKEYS = [pyxel.KEY_S,pyxel.KEY_DOWN]
LEFTKEYS = [pyxel.KEY_A,pyxel.KEY_LEFT]
RIGHTKEYS = [pyxel.KEY_D,pyxel.KEY_RIGHT]
COLLECTKEYS = [pyxel.KEY_SPACE]
XRAYKEYS = [pyxel.KEY_J]


COS45 = 0.707

def key_pressed(keygroup):
    for key in keygroup:
        if pyxel.btn(key):
            return True
    return False

class Sprite():
    def __init__(self, u, v, w, h, colkey=None) -> None:
        self.img = 0
        self.u = u
        self.v = v
        self.w = w
        self.h = h
        self.colkey = colkey

    def draw(self, x, y) -> None:
        pyxel.blt(x, y, self.img, self.u, self.v, self.w, self.h, self.colkey)
        
class Player():
    def __init__(self):
        self.x = 50
        self.y = 50

    def update(self) -> None:
        speed = PLAYER_SPEED
        if (key_pressed(UPKEYS) or key_pressed(DOWNKEYS)) and (key_pressed(RIGHTKEYS) or key_pressed(LEFTKEYS)): # we are moving diag
            speed *= COS45
        
        if key_pressed(UPKEYS):
            self.y -= speed
        
        if key_pressed(DOWNKEYS):
            self.y += speed

        if key_pressed(LEFTKEYS):
            self.x -= speed
        
        if key_pressed(RIGHTKEYS):
            self.x += speed

    def draw(self) -> None:
        pass

class Object():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self) -> None:
        pass

    def draw(self) -> None:
        pass 
    
class Screen():
    def __init__(self):
        self.objectCount = random.randint(MIN_OBJECTS_PER_SCREEN, MAX_OBJECTS_PER_SCREEN)
        self.objects = []
        self.objectCoords = []
        for _ in range(self.objectCount):
            x = random.randint(0, 15)
            y = random.randint(0, 14)
            while (x, y) in self.objectCoords:
                x = random.randint(0, 15)
                y = random.randint(0, 14)
            self.objectCoords.append((x, y))
            self.objects.append(Object(x, y))

    def draw(self) -> None:
        for obj in self.objects:
            obj.draw()

class App:
    def __init__(self):
        pyxel.init(128, 128, title="NDC 2023")
        pyxel.load("ndc.pyxres")

        pyxel.run(self.update, self.draw)

    def update(self) -> None:
        pass

    def draw(self) -> None:
        pyxel.text(55, 41, "Hello, world!", pyxel.frame_count % 16)

game = App()