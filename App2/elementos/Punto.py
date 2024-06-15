# elementos/Punto.py

class Punto:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.cubierto = False

    def marcar_cubierto(self):
        self.cubierto = True

    def esta_cubierto(self):
        return self.cubierto
