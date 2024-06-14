from elements.Pixel import Pixel

class Terreno:
    def __init__(self, lado):
        self.lado = lado
        self.pixels = [[Pixel(x, y) for y in range(lado)] for x in range(lado)]

    def agregar_aspersor(self, aspersor):
        for fila in self.pixels:
            for pixel in fila:
                if aspersor.cubre(pixel):
                    pixel.cubrir()

    def area_cubierta(self):
        return sum(pixel.esta_cubierto() for fila in self.pixels for pixel in fila)

    def __repr__(self):
        return f"Terreno(lado={self.lado})"
