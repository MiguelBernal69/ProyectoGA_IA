from shapely.geometry import Point, Polygon
from shapely.ops import unary_union
import numpy as np

# Configuración inicial global
NUM_ASPERSORES = 5
RADIO_ASPERSOR = 1.5
AREA_TOTAL = Polygon([(0, 0), (10, 0), (10, 10), (0, 10)])
PENALIZACION = 0.1
TAM_POBLACION = 10
NUM_GENERACIONES = 50

current_generation = 0

def inicializar_poblacion():
    return [[(np.random.uniform(0, 10), np.random.uniform(0, 10)) for _ in range(NUM_ASPERSORES)] for _ in range(TAM_POBLACION)]

def calcular_fitness(individuo):
    aspersores = [Point(x, y).buffer(RADIO_ASPERSOR) for x, y in individuo]
    area_cubierta = unary_union(aspersores)
    area_regada = area_cubierta.intersection(AREA_TOTAL).area
    area_no_cubierta = AREA_TOTAL.area - area_regada
    return area_regada - area_no_cubierta * PENALIZACION

def seleccion(poblacion, fitnesses):
    total_fitness = sum(fitnesses)
    probs = [f / total_fitness for f in fitnesses]
    indices = np.random.choice(len(poblacion), size=TAM_POBLACION, replace=True, p=probs)
    return [poblacion[i] for i in indices]

def cruzamiento(padre1, padre2):
    hijo = [padre1[i] if np.random.rand() > 0.5 else padre2[i] for i in range(len(padre1))]
    return hijo

def mutacion(individuo):
    mutado = [(x + np.random.uniform(-0.5, 0.5), y + np.random.uniform(-0.5, 0.5)) if np.random.rand() < 0.1 else (x, y) for x, y in individuo]
    return mutado

def algoritmo_genetico_paso_a_paso(poblacion):
    global current_generation
    fitnesses = [calcular_fitness(individuo) for individuo in poblacion]
    poblacion = seleccion(poblacion, fitnesses)
    nueva_poblacion = []
    for i in range(0, TAM_POBLACION, 2):
        hijo1 = cruzamiento(poblacion[i], poblacion[(i + 1) % TAM_POBLACION])
        hijo2 = cruzamiento(poblacion[(i + 1) % TAM_POBLACION], poblacion[i])
        nueva_poblacion.append(mutacion(hijo1))
        nueva_poblacion.append(mutacion(hijo2))
    current_generation += 1
    finished = current_generation >= NUM_GENERACIONES
    return nueva_poblacion, finished