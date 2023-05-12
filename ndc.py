from math import sqrt
import pyxel
import random

"""
DOCUMENTATION GOES HERE
"""

MIN_OBJECTS_PER_SCREEN = 100
MAX_OBJECTS_PER_SCREEN = 140
COLLECTION_RADIUS = 5
PLAYER_SPEED = 2

UP_KEYS = [pyxel.KEY_W,pyxel.KEY_UP]
DOWN_KEYS = [pyxel.KEY_S,pyxel.KEY_DOWN]
LEFT_KEYS = [pyxel.KEY_A,pyxel.KEY_LEFT]
RIGHT_KEYS = [pyxel.KEY_D,pyxel.KEY_RIGHT]
COLLECT_KEYS = [pyxel.KEY_SPACE]
XRAY_KEYS = [pyxel.KEY_J]


COS_45 = 0.707

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

TURTLE_SMALL_1 = Sprite(0,0,9,9,0)
        
class Player():
    def __init__(self):
        self.x = 50
        self.y = 50

    def update(self) -> None:
        speed = PLAYER_SPEED
        if (key_pressed(UP_KEYS) or key_pressed(DOWN_KEYS)) and (key_pressed(RIGHT_KEYS) or key_pressed(LEFT_KEYS)): # we are moving diag
            speed *= COS_45
        
        if key_pressed(UP_KEYS):
            self.y -= speed
        
        if key_pressed(DOWN_KEYS):
            self.y += speed

        if key_pressed(LEFT_KEYS):
            self.x -= speed
        
        if key_pressed(RIGHT_KEYS):
            self.x += speed

    def draw(self) -> None:
        TURTLE_SMALL_1.draw(self.x,self.y)

class Object():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = 0

    def collect(self) -> int:
        pass # return the amount of points related to the type of object

    def draw(self) -> None:
        pass # add drawing the proper sprite
    
class Screen():
    def __init__(self, id):
        self.id = id
        self.tilemap = 0
        self.objectCount = random.randint(MIN_OBJECTS_PER_SCREEN, MAX_OBJECTS_PER_SCREEN)
        self.objects = {}
        for _ in range(self.objectCount):
            x = random.randint(0, 15)
            y = random.randint(0, 14)
            while (x, y) in self.objects:
                x = random.randint(0, 15)
                y = random.randint(0, 14)
            self.objects[(x, y)] = Object(x, y)

    def collect(self, x, y) -> int:
        if len(self.objects) == 0:
            return 0
        closestDist = float("inf")
        closest = ()
        for coords in self.objects.keys():
            dist = sqrt((coords[0]*8+4 - x)**2 + (coords[1]*8+4 - y)**2) # Take the distance between the player and the middle of the object tile
            if dist < closestDist:
                closest = coords
                closestDist = dist
        return self.objects[closest].collect() if closestDist <= COLLECTION_RADIUS else 0


    def draw(self) -> None: # also add drawing the proper tile map
        for obj in self.objects:
            obj.draw()

class App:
    def __init__(self):
        pyxel.init(128, 128, title="NDC 2023")
        pyxel.load("ndc.pyxres")

        self.player = Player()

        pyxel.run(self.update, self.draw)

    def update(self) -> None:
        self.player.update()

    def draw(self) -> None:
        pyxel.cls(0)
        self.player.draw()

game = App()