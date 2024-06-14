class Pixel:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.cubierto = False

    def cubrir(self):
        self.cubierto = True

    def esta_cubierto(self):
        return self.cubierto

    def __repr__(self):
        return f"Pixel(x={self.x}, y={self.y}, cubierto={self.cubierto})"
