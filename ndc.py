from math import sqrt
import pyxel
import random

"""
DOCUMENTATION GOES HERE
"""

MIN_OBJECTS_PER_SCREEN = 10
MAX_OBJECTS_PER_SCREEN = 14
COLLECTION_RADIUS = 5
PLAYER_SPEED = 2

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
            if self.current_screen.type == "START":
                self.x = 0
            else:
                self.x = 128
                transitionStatus = "goLeft"
        
        if self.x > 128:
            if self.current_screen.type == "END":
                self.x = 128
            else:
                self.x = 0
                transitionStatus = "goRight"

        # the interactions
        if key_pressed(COLLECT_KEYS):
            self.current_screen.collect(self.x,self.y)

        return transitionStatus

    def draw(self) -> None:
        TURTLE_SMALL_1.draw(self.x,self.y)

class Object():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = 0
        self.sprite = CRAB

    def collect(self) -> int:
        pass # return the amount of points related to the type of object

    def draw(self) -> None:
        self.sprite.draw(self.x*8, self.y*8)
    
class Screen():
    def __init__(self, id, inputType): # Types are "BOTTOM", "TOP", "NORMAL", "START", "END"
        self.id = id
        self.tilemap = 0
        self.type = inputType # Change later
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


    def draw(self) -> None:
        pyxel.rect(0, 0, 128, 120, 10)
        for obj in self.objects.values():
            obj.draw()

class App:
    def __init__(self):
        pyxel.init(128, 128, title="NDC 2023")
        pyxel.load("ndc.pyxres")

        self.screens = {}

        for i in range(1,SCREEN_COUNT+1):
            self.screens[str(i)] = Screen(str(i),"NORMAL")

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
        
        self.current_screen = self.screens[self.current_screen_id]
        self.player.update_current_screen(self.current_screen)



    def draw(self) -> None:
        pyxel.cls(0)
        self.current_screen.draw()
        self.player.draw()

game = App()