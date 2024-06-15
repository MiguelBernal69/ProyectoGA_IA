import math

class Punto:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def rotate(self, grados, xPuntoRotar, yPuntoRotar):
        radianes = math.radians(grados)
        seno = math.sin(radianes)
        coseno = math.cos(radianes)
        auxX = self.x
        auxY = self.y
        xvar = (xPuntoRotar + (auxX - xPuntoRotar) * coseno - (auxY - yPuntoRotar) * seno)
        yvar = (yPuntoRotar + (auxX - xPuntoRotar) * seno + (auxY - yPuntoRotar) * coseno)
        self.x = xvar
        self.y = yvar

    def translate(self, dx, dy):
        self.x += dx
        self.y += dy

    def equals(self, other):
        if isinstance(other, Punto):
            return other.x == self.x and other.y == self.y
        return False

    def __str__(self):
        return f"({self.x:.2f}, {self.y:.2f})"
