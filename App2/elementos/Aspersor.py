# elementos/Aspersor.py

import math

class Aspersor:
    def __init__(self, x, y, radio):
        self.x = x
        self.y = y
        self.radio = radio

    def cubre_punto(self, punto):
        distancia = math.sqrt((self.x - punto.x)**2 + (self.y - punto.y)**2)
        return distancia <= self.radio
