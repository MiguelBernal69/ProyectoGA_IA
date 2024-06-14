import math

class Aspersor:
    def __init__(self, x, y, radio):
        self.x = x
        self.y = y
        self.radio = radio

    def cubre(self, pixel):
        # Verifica si un píxel está dentro del área cubierta por el aspersor
        distancia = math.sqrt((pixel.x - self.x) ** 2 + (pixel.y - self.y) ** 2)
        return distancia <= self.radio

    def __repr__(self):
        return f"Aspersor(x={self.x}, y={self.y}, radio={self.radio})"
