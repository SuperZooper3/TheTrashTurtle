from math import sqrt
from typing import Dict, List, Tuple
import pyxel
import random

"""
Bienvenue à la plage ! Les bébés tortues ne vont pas tarder à éclore de leurs œufs. Vous êtes la maman tortue, 
"The Trash Turtle", chargée de nettoyer la plage et de dégager le chemin pour que vos bébés puissent atteindre 
l'océan en toute sécurité. Vous pouvez vous déplacer à l'aide des touches WASD ou les flèches. Pour ramasser les 
déchets sur la plage, appuyez sur la touche ESPACE. Plusieurs mécanismes se révéleront à vous si vous tentez de 
jouer plusieurs fois. Déplacez vous vers la droite pour explorer la plage. Ramassez le plus de déchets possible et 
voyez votre sac-poubelle augmenter pour sauver tous les bébés tortues ! Bonne chance !
"""

MIN_OBJECTS_PER_SCREEN = 7
MAX_OBJECTS_PER_SCREEN = 9
MIN_HIDDEN_OBJECTS_PER_SCREEN = 5
MAX_HIDDEN_OBJECTS_PER_SCREEN = 7
COLLECTION_RADIUS = 10
PLAYER_SPEED = 2
SMALL_TURTLE_SPEED = 1
XRAY_DURATION = 60 # Frames
PLAYER_POSITION_OFFSET = (4, 4)
SMALL_TURTLE_POSITION_OFFSET = (4, 4)
OBJECT_POSITION_OFFSET = (5, 5)
OBJECT_POINTS = 1
SMALL_TURTLE_STOP = 160
MAX_SMALL_TURTLES = 50

ADDITIONAL_NORMAL_SCREENS = 1 # THIS DOES NOT INCLUDE FIRST AND FINAL SCREEN, OR THE FIRST 2 NORMAL SCREENS
UP_SCREENS = 3 # NOT COUNTED IN NORMAL SCREENS

FRAMES_PER_BIG_WALK = 10
FRAMES_PER_SMALL_WALK = 10

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

INTRO_TEXT = "Bienvenue à la plage ! Les bébés tortues ne vont pas tarder à éclore de leurs œufs. Vous êtes la maman tortue, 'The Trash Turtle', chargée de nettoyer la plage et de dégager le chemin pour que vos bébés puissent atteindre l'océan en toute sécurité. Vous pouvez vous déplacer à l'aide des touches WASD ou les flèches. Pour ramasser les déchets sur la plage, appuyez sur la touche ESPACE. Plusieurs mécanismes se révéleront à vous si vous tentez de jouer plusieurs fois. Déplacez vous vers la droite pour explorer la plage. Ramassez le plus de déchets possible et voyez votre sac-poubelle augmenter pour sauver tous les bébés tortues ! Bonne chance !"
XRAY_TEXT = "Essayez de jouer à nouveau et appuyez sur la touche J pour utiliser vos pouvoirs X-RAY et révéler plus de déchets."
GO_UP_TEXT = "Essayez de jouer à nouveau et quand vous voyez un trèfle à quatre feuilles déplacez-vous vers le haut pour découvrir un espace secret de la plage."
ALL_W_TEXT = "Vous avez découvert tous les secrets de la plage et vous avez réussi à trouver tous les déchets ! Bien joué !"
FINAL_TEXT = "Félicitations, vous avez ramassé THIS MUCH déchets ! Mais il reste encore beaucoup de déchets sur terre. Nous devons faire attention à ne pas laisser de déchets sur la plage ou dans l'océan, car cela peut nuire aux tortues. Nous pouvons tous aider à sauver les tortues en faisant notre part pour protéger l'environnement et les océans."

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

BIG_TURTULE_1_RIGHT = Sprite(48,0,16,16,0)
BIG_TURTULE_2_RIGHT = Sprite(48,16,16,16,0)

BIG_TURTULE_1_LEFT = Sprite(48,32,16,16,0)
BIG_TURTULE_2_LEFT = Sprite(64,32,16,16,0)

BIG_TURTULE_1_UP = Sprite(48,48,16,16,0)
BIG_TURTULE_2_UP = Sprite(64,48,16,16,0)

BIG_TURTULE_1_DOWN = Sprite(64,0,16,16,0)
BIG_TURTULE_2_DOWN = Sprite(64,16,16,16,0)

BIG_TURTULES = [[BIG_TURTULE_1_RIGHT,BIG_TURTULE_2_RIGHT],[BIG_TURTULE_1_LEFT,BIG_TURTULE_2_LEFT],[BIG_TURTULE_1_UP,BIG_TURTULE_2_UP],[BIG_TURTULE_1_DOWN,BIG_TURTULE_2_DOWN]]

TRASH_BAG_1 = Sprite(16,72,16,16,7)
TRASH_BAG_2 = Sprite(32,72,16,16,7)
TRASH_BAG_3 = Sprite(0,72,16,16,7)
TRASH_BAG_4 = Sprite(0,88,16,16,7)
TRASH_BAG_5 = Sprite(16,88,16,16,7)
TRASH_BAG_GOLDEN = Sprite(16,224,16,16,7)

TRASH_BAGS = [TRASH_BAG_1, TRASH_BAG_2, TRASH_BAG_3, TRASH_BAG_4, TRASH_BAG_5, TRASH_BAG_GOLDEN]

SODA_CAN = Sprite(0,152,10,10,7)
X_SODA_CAN = Sprite(0,163,10,10,7)

STRAWS = Sprite(0,174,10,10,7)
X_STRAWS = Sprite(0,185,10,10,7)

CIG = Sprite(0,196,10,10,7)
X_CIG = Sprite(0,207,10,10,7)

CLOVER = Sprite(24,168,10,10,7)

GARBAGE_CAN = Sprite(0,224,16,16,11)

CRAB = Sprite(0, 28, 8, 7)

NORMAL_SPRITES = [SODA_CAN, STRAWS, CIG]
HIDDEN_SPRITES = [X_SODA_CAN, X_STRAWS, X_CIG]
        
class Player():
    def __init__(self, screen, totalTrash):
        self.x = 50
        self.y = 50
        self.current_screen = screen
        self.lastDirection = 0 # 0 is right 1 is left 2 is up 3 is down
        self.points = 0
        self.totalTrash = totalTrash

        self.hasXrayed = False
        self.hasUped = False
        self.noBag = False

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
            if not self.current_screen.type == "DOWN": # if there is no above transition, clip the y
                self.y = 0
            else: # we're going to transition next frame
                self.y = 120 # start at the bottom of the screen
                transitionStatus = "goUp"
                self.hasUped = True
        
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

            if self.current_screen.type == "END" and self.x > 60 and (self.y < 20 or self.y > 80): # Trigger the final cutscene
                transitionStatus = "cutscene"
                self.noBag = True
        
        if key_pressed(XRAY_KEYS):
            self.current_screen.xray()
            self.hasXrayed = True

        return transitionStatus, self.points

    def draw(self) -> None:
        BIG_TURTULES[self.lastDirection][int(pyxel.frame_count/FRAMES_PER_BIG_WALK)%len(BIG_TURTULES[self.lastDirection])].draw(self.x-PLAYER_POSITION_OFFSET[0],self.y-PLAYER_POSITION_OFFSET[1])
        trashIndex = int((len(TRASH_BAGS)-1)*self.points/self.totalTrash)
        if not self.noBag:
            TRASH_BAGS[trashIndex].draw(self.x-4,self.y-8)

class Object():
    def __init__(self, x, y, clover, hidden=False):
        self.x = x
        self.y = y
        self.hidden = hidden
        self.clover = clover
        if clover:
            self.sprite = CLOVER
        elif not hidden:
            self.sprite = random.choice(NORMAL_SPRITES)
        else:
            self.sprite = random.choice(HIDDEN_SPRITES)

    def collect(self) -> int:
        return OBJECT_POINTS

    def draw(self) -> None:
        self.sprite.draw(self.x*10+4, self.y*10+5)
    
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
            if self.type == "DOWN":
                x = random.randint(0, 11)
                y = random.randint(0, 10)
                self.objects[(x, y)] = Object(x, y, True, False)
            for _ in range(self.objectCount):
                if len(self.objects) >= 132:
                    break
                x = random.randint(0, 11)
                y = random.randint(0, 10)
                while (x, y) in self.objects:
                    x = random.randint(0, 11)
                    y = random.randint(0, 10)
                self.objects[(x, y)] = Object(x, y, False, False)
            self.hiddenObjectCount = random.randint(MIN_HIDDEN_OBJECTS_PER_SCREEN, MAX_HIDDEN_OBJECTS_PER_SCREEN)
            for _ in range(self.hiddenObjectCount):
                if len(self.objects) >= 132:
                    break
                x = random.randint(0, 11)
                y = random.randint(0, 10)
                while (x, y) in self.objects:
                    x = random.randint(0, 11)
                    y = random.randint(0, 10)
                self.objects[(x, y)] = Object(x, y, 0, True)
            self.trashCount = len(self.objects)
        else:
            self.trashCount = 0

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
                dist = sqrt((coords[0]*10+4+OBJECT_POSITION_OFFSET[0] - x)**2 + (coords[1]*10+5+OBJECT_POSITION_OFFSET[1] - y)**2) # Take the distance between the player and the middle of the object tile
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

        pyxel.text(1,121,SCREEN_TEXTS.get(self.id,""),0)


class SmallTurtle:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.speed = SMALL_TURTLE_SPEED
    
    def update(self):
        self.x += self.speed
        if self.x >= SMALL_TURTLE_STOP:
            self.speed = 0
    
    def draw(self) -> None:
        SMALL_TURTULES[int(pyxel.frame_count/FRAMES_PER_SMALL_WALK)%len(SMALL_TURTULES)].draw(self.x-SMALL_TURTLE_POSITION_OFFSET[0],self.y-SMALL_TURTLE_POSITION_OFFSET[1])


class Cutscene:
    def __init__(self, numTurtles) -> None:
        self.over = False
        self.smallTurtles: List[SmallTurtle] = []
        for _ in range(numTurtles):
            self.smallTurtles.append(SmallTurtle(random.randint(-305, -5), random.randint(25, 95)))
    
    def update(self) -> None:
        for turtle in self.smallTurtles:
            turtle.update()
        for turtle in self.smallTurtles:
            if turtle.speed != 0:
                break
        else:
            self.over = True
    
    def draw(self) -> None:
        for turtle in self.smallTurtles:
            turtle.draw()


class App:
    def __init__(self):
        pyxel.init(128, 128, title="NDC 2023")
        pyxel.load("ndc.pyxres")

        self.screens: Dict[str, Screen] = {}
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

        self.totalTrash = 0
        for screen in self.screens.values():
            self.totalTrash += screen.trashCount

        self.current_screen_id = "0"
        self.current_screen = self.screens[self.current_screen_id]
        self.player = Player(self.current_screen,self.totalTrash)

        self.started = False
        self.finished = False
        self.playerControl = False
        self.cutscenePlaying = False
        self.cutscene = Cutscene(0)

        pyxel.run(self.update, self.draw)

    def update(self) -> None:
        if self.started and not self.cutscenePlaying:
            if self.playerControl: 
                transitionStatus,points = self.player.update()
                if transitionStatus == "goRight":
                    self.current_screen_id = str(int(self.current_screen_id) + 1)

                if transitionStatus == "goLeft":
                    self.current_screen_id = str(int(self.current_screen_id) - 1)
                
                if transitionStatus == "goUp":
                    self.current_screen_id = self.current_screen_id + "*"

                if transitionStatus == "goDown":
                    self.current_screen_id = self.current_screen_id[:-1]

                if transitionStatus == "cutscene": # they've triggered the end of the game
                    self.playerControl = False
                    self.cutscenePlaying = True
                    self.cutscene = Cutscene(int(MAX_SMALL_TURTLES*points/self.totalTrash))
            
            self.current_screen = self.screens[self.current_screen_id]
            self.player.update_current_screen(self.current_screen)
        elif self.cutscenePlaying: 
            self.cutscene.update()
        else:
            if key_pressed(COLLECT_KEYS):
                self.started = True
                self.playerControl = True
            

    def draw(self) -> None:
        pyxel.cls(0)
        self.current_screen.draw()

        if self.cutscenePlaying:
            self.cutscene.draw()
            if self.cutscene.over:
                self.finished = True

        self.player.draw()

        if not self.started:
            pyxel.rect(10,10,110,100,0)
            pyxel.text(12,12,INTRO_TEXT,7)

        if self.finished:
            pyxel.rect(10,10,110,100,0)
            # Write text depending 
            finalText = "final text here"
            if not self.player.hasXrayed:
                finalText = XRAY_TEXT
            elif not self.player.hasUped:
                finalText = GO_UP_TEXT
            else:
                finalText = ALL_W_TEXT
            pyxel.text(12,12,FINAL_TEXT,7)
            pyxel.text(12,70,finalText,7)
            

game = App()