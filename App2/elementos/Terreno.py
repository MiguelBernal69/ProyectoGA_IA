# elementos/Terreno.py

from elementos.Punto import Punto

class Terreno:
    def __init__(self, lado, tam_punto):
        self.lado = lado
        self.tam_punto = tam_punto
        self.puntos = [
            [Punto(x, y) for y in range(0, lado, tam_punto)]
            for x in range(0, lado, tam_punto)
        ]

    def agregar_aspersor(self, aspersor):
        for fila in self.puntos:
            for punto in fila:
                if aspersor.cubre_punto(punto):
                    punto.marcar_cubierto()

    def area_cubierta(self):
        total_puntos = sum([len(fila) for fila in self.puntos])
        puntos_cubiertos = sum([punto.esta_cubierto() for fila in self.puntos for punto in fila])
        return puntos_cubiertos / total_puntos
