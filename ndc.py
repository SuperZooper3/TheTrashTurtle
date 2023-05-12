import pyxel
import random

"""
DOCUMENTATION GOES HERE
"""

MIN_OBJECTS_PER_SCREEN = 100
MAX_OBJECTS_PER_SCREEN = 140

class Sprite():
    def __init__(self) -> None:
        pass

    def draw(self):
        pass

class Player():
    def __init__(self):
        pass

    def update(self) -> None:
        pass

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