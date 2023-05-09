import pyxel

"""
DOCUMENTATION GOES HERE
"""

# Key bindings
UP_KEYS = [pyxel.KEY_UP, pyxel.KEY_W]
DOWN_KEYS = [pyxel.KEY_DOWN, pyxel.KEY_S]
LEFT_KEYS = [pyxel.KEY_LEFT, pyxel.KEY_A]
RIGHT_KEYS = [pyxel.KEY_RIGHT, pyxel.KEY_D]


def input_pressed(key_list):
    for k in key_list:
        if pyxel.btn(k):
            return True
    return False


class Sprite:
    def __init__(self, sheetX: int, sheetY: int, sheetW: int, sheetH: int, colourKey: int = 0):
        self.sheetX = sheetX
        self.sheetY = sheetY
        self.sheetW = sheetW
        self.sheetH = sheetH
        self.colKey = colourKey
        self.sheet = 0

    def draw(self, x: int, y: int) -> None:
        pyxel.blt(x, y, self.sheet, self.sheetX, self.sheetY,
                  self.sheetW, self.sheetH, self.colKey)
        
# COPY PASTED FROM LAST YEAR'S CODE
class ComplexSprite:
    def __init__(self, seedSprite, sproutSprite, grownSprite, deadSprite):
        self.seedSprite = seedSprite
        self.sproutSprite = sproutSprite
        self.grownSprite = grownSprite
        self.deadSprite = deadSprite

    def draw(self, x, y, n):  # n = 0 for seed, n = 1 for sprout, n = 2 for grown, n = 3 for dead
        if n == 0:
            self.seedSprite.draw(x, y)
        elif n == 1:
            self.sproutSprite.draw(x, y)
        elif n == 2:
            self.grownSprite.draw(x, y)
        elif n == 3:
            self.deadSprite.draw(x, y)
        else:
            print("plantSpriteDrawError")


testSprite = Sprite(0, 0, 16, 16)

class App:
    def __init__(self):
        pyxel.init(128, 128, title="NDC 2023")
        pyxel.load("NDC2023.pyxres")

        pyxel.run(self.update, self.draw)

    def update(self) -> None:
        pass

    def draw(self) -> None:
        pyxel.text(55, 41, "Hello, world!", pyxel.frame_count % 16)
        testSprite.draw(0, 0)


game = App()