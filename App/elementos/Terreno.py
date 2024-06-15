# elementos/Terreno.py

import math
from elementos.Aspersor import Aspersor

class Terreno:
    def __init__(self, lado):
        self.lado = lado
        self.aspersiones = []

    def agregar_aspersor(self, aspersor):
        self.aspersiones.append(aspersor)

    def area_cubierta(self):
        area_total = self.lado * self.lado
        area_cubierta = 0
        for x in range(self.lado):
            for y in range(self.lado):
                if any(aspersor.cubre_punto(x, y) for aspersor in self.aspersiones):
                    area_cubierta += 1
        return area_cubierta / area_total

    def penalizacion_no_cubierta(self):
        area_total = self.lado * self.lado
        area_no_cubierta = 0
        for x in range(self.lado):
            for y in range(self.lado):
                if not any(aspersor.cubre_punto(x, y) for aspersor in self.aspersiones):
                    area_no_cubierta += 1
        return area_no_cubierta / area_total

    def penalizacion_superposicion(self):
        superposicion = 0
        for i, aspersor1 in enumerate(self.aspersiones):
            for aspersor2 in self.aspersiones[i+1:]:
                distancia = math.sqrt((aspersor1.x - aspersor2.x)**2 + (aspersor1.y - aspersor2.y)**2)
                if distancia < aspersor1.radio + aspersor2.radio:
                    superposicion += (aspersor1.radio + aspersor2.radio - distancia) / (aspersor1.radio + aspersor2.radio)
        return superposicion

    def fitness(self):
        return self.area_cubierta() - self.penalizacion_no_cubierta() - self.penalizacion_superposicion()
