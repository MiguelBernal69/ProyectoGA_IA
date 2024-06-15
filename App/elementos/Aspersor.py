# elementos/Aspersor.py

class Aspersor:
    def __init__(self, x, y, radio):
        self.x = x
        self.y = y
        self.radio = radio

    def cubre_punto(self, px, py):
        return (self.x - px)**2 + (self.y - py)**2 <= self.radio**2
