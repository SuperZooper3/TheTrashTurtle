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
OBJECT_POINTS = 1

ADDITIONAL_NORMAL_SCREENS = 2 # THIS DOES NOT INCLUDE FIRST AND FINAL SCREEN, OR THE FIRST 2 NORMAL SCREENS
UP_SCREENS = 1 # NOT COUNTED IN NORMAL SCREENS

UP_KEYS = [pyxel.KEY_W,pyxel.KEY_UP]
DOWN_KEYS = [pyxel.KEY_S,pyxel.KEY_DOWN]
LEFT_KEYS = [pyxel.KEY_A,pyxel.KEY_LEFT]
RIGHT_KEYS = [pyxel.KEY_D,pyxel.KEY_RIGHT]
COLLECT_KEYS = [pyxel.KEY_SPACE]
XRAY_KEYS = [pyxel.KEY_J]


COS_45 = 0.707

SCREEN_TEXTS = {
    "0":"A",
    "1":"B",
    "2":"C",
    "3":"D",
    }

XRAY_TEXT = "xray text goes here"
GO_UP_TEXT = "go up text goes here"

# make sure to buffer the screen texts so that 

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

class Tilemap():
    def __init__(self, tm, u, v, w=128, h=128) -> None:
        self.tm = tm
        self.u = u
        self.v = v
        self.w = w
        self.h = h

    def draw(self, x, y) -> None:
        pyxel.bltm(x, y, self.tm, self.u, self.v, self.w, self.h)

NORMAL_TILEMAP_1 = Tilemap(0,0,0)
START_TILEMAP = Tilemap(0,0,128)
END_TILEMAP = Tilemap(0,128,0)

NORMAL_TILEMAPS = [NORMAL_TILEMAP_1]

TURTLE_SMALL_1 = Sprite(0,0,9,9,0)
TURTLE_SMALL_2 = Sprite(0,10,7,9,0)
TURTLE_SMALL_3 = Sprite(0,18,9,9,0)

SMALL_TURTULES = [TURTLE_SMALL_1,TURTLE_SMALL_2,TURTLE_SMALL_3]

BIG_TURTULE_1 = Sprite(10,0,14,9,0)
BIG_TURTULE_2 = Sprite(10,12,14,9,0)

BIG_TURTULES = [[BIG_TURTULE_1,BIG_TURTULE_2],[BIG_TURTULE_1,BIG_TURTULE_2],[BIG_TURTULE_1,BIG_TURTULE_2],[BIG_TURTULE_1,BIG_TURTULE_2]]

FRAMES_PER_BIG_WALK = 10

TRASH_BAG_1 = Sprite(17,82,7,6,7)

TRASH_BAGS = [TRASH_BAG_1]

CRAB = Sprite(0, 28, 8, 7)
        
class Player():
    def __init__(self, screen):
        self.x = 50
        self.y = 50
        self.current_screen = screen
        self.lastDirection = 0 # 0 is right 1 is left 2 is up 3 is down
        self.points = 0

    def update_current_screen(self,screen):
        self.current_screen = screen
        
    def update(self):
        speed = PLAYER_SPEED
        if (key_pressed(UP_KEYS) or key_pressed(DOWN_KEYS)) and (key_pressed(RIGHT_KEYS) or key_pressed(LEFT_KEYS)): # we are moving diag
            speed *= COS_45
        
        if key_pressed(UP_KEYS):
            self.y -= speed
            self.lastDirection = 2
        
        if key_pressed(DOWN_KEYS):
            self.y += speed
            self.lastDirection = 3

        if key_pressed(LEFT_KEYS):
            self.x -= speed
            self.lastDirection = 1
        
        if key_pressed(RIGHT_KEYS):
            self.x += speed
            self.lastDirection = 0

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
            self.current_screen.collect(self.x,self.y)
        
        if key_pressed(XRAY_KEYS):
            self.current_screen.xray()

        return transitionStatus

    def draw(self) -> None:
        BIG_TURTULES[self.lastDirection][int(pyxel.frame_count/FRAMES_PER_BIG_WALK)%len(BIG_TURTULES[self.lastDirection])].draw(self.x-PLAYER_POSITION_OFFSET,self.y-PLAYER_POSITION_OFFSET)
        TRASH_BAGS[0].draw(self.x-PLAYER_POSITION_OFFSET,self.y-PLAYER_POSITION_OFFSET)


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
        self.type = inputType
        self.scan = False
        self.scanEnd = -1
        if self.type == "START":
            self.tilemap = START_TILEMAP
        elif self.type == "END":
            self.tilemap = END_TILEMAP
        else:
            self.tilemap = random.choice(NORMAL_TILEMAPS)
        if self.type not in ("START", "END"):
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
        if self.type not in ("START", "END"):
            self.scanEnd = pyxel.frame_count + XRAY_DURATION
            self.scan = True

    def collect(self, x, y) -> int:
        if self.type not in ("START", "END"):
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
        self.tilemap.draw(0, 0)
        if self.type not in ("START", "END"):
            for obj in self.objects.values():
                if (obj.hidden and pyxel.frame_count <= self.scanEnd) or not obj.hidden:
                    obj.draw()

        pyxel.text(0,120,SCREEN_TEXTS.get(self.id,""),0)

class App:
    def __init__(self):
        pyxel.init(128, 128, title="NDC 2023")
        pyxel.load("ndc.pyxres")

        self.screens = {}
        for i in range(1, 3):
            self.screens[str(i)] = Screen(str(i), "NORMAL")
        if ADDITIONAL_NORMAL_SCREENS + UP_SCREENS > 0:
            screenOrder = ["NORMAL"]*ADDITIONAL_NORMAL_SCREENS + ["DOWN"]*UP_SCREENS
            random.shuffle(screenOrder)
            for i, type in enumerate(screenOrder, start=3):
                self.screens[str(i)] = Screen(str(i), type)
                if type == "DOWN":
                    self.screens[f"{i}*"] = Screen(f"{i}*", "UP")

        # Add the first and last screens that will be special, but thats later
        self.screens["0"] = Screen("0","START")
        self.screens[str(UP_SCREENS+ADDITIONAL_NORMAL_SCREENS+3)] = Screen(str(UP_SCREENS+ADDITIONAL_NORMAL_SCREENS+3),"END")

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