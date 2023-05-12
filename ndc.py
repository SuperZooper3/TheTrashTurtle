from math import sqrt
from typing import Dict
import pyxel
import random

"""
DOCUMENTATION GOES HERE
"""

MIN_OBJECTS_PER_SCREEN = 10
MAX_OBJECTS_PER_SCREEN = 14
MIN_HIDDEN_OBJECTS_PER_SCREEN = 10
MAX_HIDDEN_OBJECTS_PER_SCREEN = 14
COLLECTION_RADIUS = 5
PLAYER_SPEED = 2
XRAY_DURATION = 60 # Frames

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
CRAB = Sprite(0, 28, 8, 7)
        
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
    def __init__(self, x, y, inputType, hidden=False):
        self.x = x
        self.y = y
        self.hidden = hidden
        self.type = inputType
        self.sprite = CRAB

    def collect(self) -> int:
        return 10

    def draw(self) -> None:
        self.sprite.draw(self.x*8, self.y*8)
    
class Screen():
    def __init__(self, id, inputType): # Types are "BOTTOM", "TOP", "NORMAL", "START", "END"
        self.id = id
        self.tile = 0
        self.type = inputType
        self.scan = False
        self.scanEnd = -1
        self.objectCount = random.randint(MIN_OBJECTS_PER_SCREEN, MAX_OBJECTS_PER_SCREEN)
        self.objects: Dict[Object] = {}
        for _ in range(self.objectCount):
            x = random.randint(0, 15)
            y = random.randint(0, 14)
            while (x, y) in self.objects:
                x = random.randint(0, 15)
                y = random.randint(0, 14)
            self.objects[(x, y)] = Object(x, y, 0, False)
        self.hiddenObjectCount = random.randint(MIN_HIDDEN_OBJECTS_PER_SCREEN, MAX_HIDDEN_OBJECTS_PER_SCREEN)
        for _ in range(self.objectCount):
            x = random.randint(0, 15)
            y = random.randint(0, 14)
            while (x, y) in self.objects:
                x = random.randint(0, 15)
                y = random.randint(0, 14)
            self.objects[(x, y)] = Object(x, y, 0, True)

    def xray(self):
        self.scanEnd = pyxel.frame_count + XRAY_DURATION
        self.scan = True

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
        if (self.objects[closest].hidden and self.scan) or not self.objects[closest].hidden:
            return self.objects[closest].collect() if closestDist <= COLLECTION_RADIUS else 0

    def draw(self) -> None:
        pyxel.rect(0, 0, 128, 120, 10)
        for obj in self.objects.values():
            if (obj.hidden and pyxel.frame_count <= self.scanEnd) or not obj.hidden:
                obj.draw()

class App:
    def __init__(self):
        pyxel.init(128, 128, title="NDC 2023")
        pyxel.load("ndc.pyxres")

        self.player = Player()
        self.testScreen = Screen(0, "NORMAL")

        pyxel.run(self.update, self.draw)

    def update(self) -> None:
        self.player.update()

    def draw(self) -> None:
        pyxel.cls(0)
        self.player.draw()
        self.testScreen.draw()

game = App()