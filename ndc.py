from math import sqrt
from typing import Dict, Tuple
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
PLAYER_POSITION_OFFSET = 4
OBJECT_POSITION_OFFSET = 4
OBJECT_POINTS = 10

SCREEN_COUNT = 1 # THIS DOSE NOT INCLUDE FIRST AND FINAL SCREEN

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
    def __init__(self, screen):
        self.x = 50
        self.y = 50
        self.current_screen = screen
        self.points = 0

    def update_current_screen(self,screen):
        self.current_screen = screen
        
    def update(self):
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

        transitionStatus = "None"

        if self.y < 0:
            if not self.current_screen.type == "DOWN": # if there is no above transitoin, clip the y
                self.y = 0
            else: # we're going to transition next frame
                self.y = 120 # start at the bottom of the screen
                transitionStatus = "goUp"
        
        if self.y > 120: # we went past the bottom
            if not self.current_screen.type == "UP":
                self.y = 120
            else: # we're going to go down
                self.y = 0
                transitionStatus = "goDown"
        
        if self.x < 0: # FIXME: MAKE SURE TOP SCREENS CANT TRASNTION
            if self.current_screen.type == "START" or self.current_screen.type == "UP":
                self.x = 0
            else:
                self.x = 128
                transitionStatus = "goLeft"
        
        if self.x > 128:
            if self.current_screen.type == "END" or self.current_screen.type == "UP":
                self.x = 128
            else:
                self.x = 0
                transitionStatus = "goRight"

        # the interactions
        if key_pressed(COLLECT_KEYS):
            self.points += self.current_screen.collect(self.x,self.y)
            print(self.points)
            self.current_screen.collect(self.x,self.y)
        
        if key_pressed(XRAY_KEYS):
            self.current_screen.xray()

        return transitionStatus

    def draw(self) -> None:
        TURTLE_SMALL_1.draw(self.x-PLAYER_POSITION_OFFSET,self.y-PLAYER_POSITION_OFFSET)

class Object():
    def __init__(self, x, y, inputType, hidden=False):
        self.x = x
        self.y = y
        self.hidden = hidden
        self.type = inputType
        self.sprite = CRAB

    def collect(self) -> int:
        return OBJECT_POINTS

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
        self.objects: Dict[Tuple[int, int], Object] = {}
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
        closest: Tuple[int, int] = (-1, -1)
        for coords in self.objects.keys():
            dist = sqrt((coords[0]*8+OBJECT_POSITION_OFFSET - x)**2 + (coords[1]*8+OBJECT_POSITION_OFFSET - y)**2) # Take the distance between the player and the middle of the object tile
            if dist < closestDist:
                closest = coords
                closestDist = dist
        if (self.objects[closest].hidden and self.scan) or not self.objects[closest].hidden:
            if closestDist <= COLLECTION_RADIUS:
                points = self.objects[closest].collect()
                del self.objects[closest]
                return points
        return 0

    def draw(self) -> None:
        pyxel.rect(0, 0, 128, 120, 10)
        for obj in self.objects.values():
            if (obj.hidden and pyxel.frame_count <= self.scanEnd) or not obj.hidden:
                obj.draw()

class App:
    def __init__(self):
        pyxel.init(128, 128, title="NDC 2023")
        pyxel.load("ndc.pyxres")

        self.screens = {}

        for i in range(1,SCREEN_COUNT+1):
            self.screens[str(i)] = Screen(str(i),"DOWN")
        
        self.screens["1*"] = Screen("1*","UP")

        # Add the first and last sreens that will be special, but thats later
        self.screens["0"] = Screen("0","START")
        self.screens[str(SCREEN_COUNT+1)] = Screen(str(SCREEN_COUNT+1),"END")

        self.current_screen_id = "0"
        self.current_screen = self.screens[self.current_screen_id]
        self.player = Player(self.current_screen)

        print(self.screens)

        pyxel.run(self.update, self.draw)

    def update(self) -> None:
        transitionStatus = self.player.update()
        if transitionStatus == "goRight":
            self.current_screen_id = str(int(self.current_screen_id) + 1)
            print(self.current_screen_id)

        if transitionStatus == "goLeft":
            self.current_screen_id = str(int(self.current_screen_id) - 1)
            print(self.current_screen_id)
        
        if transitionStatus == "goUp":
            self.current_screen_id = self.current_screen_id + "*"
            print(self.current_screen_id)

        if transitionStatus == "goDown":
            self.current_screen_id = self.current_screen_id[:-1]
            print(self.current_screen_id)
        
        self.current_screen = self.screens[self.current_screen_id]
        self.player.update_current_screen(self.current_screen)



    def draw(self) -> None:
        pyxel.cls(0)
        self.current_screen.draw()
        self.player.draw()

game = App()