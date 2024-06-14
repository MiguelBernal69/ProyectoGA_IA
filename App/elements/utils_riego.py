import random
from App.elements.Aspersor import Aspersor

def generar_posiciones_aleatorias(num_aspersores, lado_terreno):
    posiciones = []
    for _ in range(num_aspersores):
        x = random.uniform(0, lado_terreno)
        y = random.uniform(0, lado_terreno)
        posiciones.append((x, y))
    return posiciones
