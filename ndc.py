import pyxel

"""
DOCUMENTATION GOES HERE
"""

class App:
    def __init__(self):
        pyxel.init(128, 128, title="NDC 2023")
        pyxel.load("NDC2023.pyxres")

        pyxel.run(self.update, self.draw)

    def update(self) -> None:
        pass

    def draw(self) -> None:
        pyxel.text(55, 41, "Hello, world!", pyxel.frame_count % 16)

game = App()