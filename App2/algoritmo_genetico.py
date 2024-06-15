# algoritmo_genetico.py

import random
import matplotlib.pyplot as plt
from elementos.Terreno import Terreno
from elementos.Aspersor import Aspersor

class Individuo:
    def __init__(self, genes):
        self.genes = genes
        self.fitness = None

    def evaluar(self, evaluacion_func, **kwargs):
        self.fitness = evaluacion_func(self.genes, **kwargs)
        return self.fitness

def inicializar_poblacion(tam_poblacion, longitud_gen):
    poblacion = [Individuo([random.uniform(0, 100) for _ in range(longitud_gen)]) for _ in range(tam_poblacion)]
    print(poblacion)
    return poblacion

def seleccion_torneo(poblacion, k=3):
    seleccionados = random.sample(poblacion, k)
    seleccionados.sort(key=lambda ind: ind.fitness, reverse=True)
    return seleccionados[0]

def cruce_uniforme(padre1, padre2):
    hijo1_genes, hijo2_genes = [], []
    for g1, g2 in zip(padre1.genes, padre2.genes):
        if random.random() < 0.5:
            hijo1_genes.append(g1)
            hijo2_genes.append(g2)
        else:
            hijo1_genes.append(g2)
            hijo2_genes.append(g1)
    return Individuo(hijo1_genes), Individuo(hijo2_genes)

def mutacion_uniforme(individuo, prob_mutacion):
    for i in range(len(individuo.genes)):
        if random.random() < prob_mutacion:
            individuo.genes[i] = random.uniform(0, 100)

def evaluar_terreno(genes, lado_terreno, tam_punto, radio_aspersor):
    terreno = Terreno(lado_terreno, tam_punto)
    for i in range(0, len(genes), 2):
        aspersor = Aspersor(genes[i], genes[i + 1], radio_aspersor)
        terreno.agregar_aspersor(aspersor)
    return terreno.area_cubierta()

def graficar_terreno(ax, individuo, radio_aspersor, iteracion, lado_terreno, tam_punto, area_cubierta):
    ax.clear()
    ax.set_aspect('equal')
    plt.xlim(0, lado_terreno)
    plt.ylim(0, lado_terreno)

    # Dibujar el terreno
    rect_terreno = plt.Rectangle((0, 0), lado_terreno, lado_terreno, fill=None, edgecolor='r')
    ax.add_patch(rect_terreno)

    # Dibujar los aspersores
    aspersores = [Aspersor(individuo.genes[i], individuo.genes[i + 1], radio_aspersor) for i in range(0, len(individuo.genes), 2)]
    for aspersor in aspersores:
        circle = plt.Circle((aspersor.x, aspersor.y), radio_aspersor, fill=True, edgecolor='b', alpha=0.5)
        ax.add_patch(circle)
    
    # Mostrar el número de iteración
    ax.text(0.95, 0.05, f'Iteración: {iteracion}', horizontalalignment='right', verticalalignment='center', transform=ax.transAxes, fontsize=12, bbox=dict(facecolor='white', alpha=0.5))
    
    # Mostrar el área cubierta
    ax.text(0.05, 0.05, f'Área cubierta: {area_cubierta:.2f}', horizontalalignment='left', verticalalignment='center', transform=ax.transAxes, fontsize=12, bbox=dict(facecolor='white', alpha=0.5))

def calcular_estadisticas(poblacion):
    fitness_values = [ind.fitness for ind in poblacion]
    min_fitness = min(fitness_values)
    max_fitness = max(fitness_values)
    avg_fitness = sum(fitness_values) / len(fitness_values)
    return min_fitness, max_fitness, avg_fitness

def algoritmo_genetico(tam_poblacion, longitud_gen, num_generaciones, prob_mutacion, evaluacion_func, **kwargs):
    poblacion = inicializar_poblacion(tam_poblacion, longitud_gen)

    for individuo in poblacion:
        individuo.evaluar(evaluacion_func, **kwargs)

    # Configuración de la gráfica
    fig, ax = plt.subplots()
    plt.ion()
    plt.show()

    mejor_individuo = None
    area_maxima = kwargs['lado_terreno'] ** 2  # Área máxima del terreno

    for gen in range(num_generaciones):
        nueva_poblacion = []
        for _ in range(tam_poblacion // 2):
            padre1 = seleccion_torneo(poblacion)
            padre2 = seleccion_torneo(poblacion)
            hijo1, hijo2 = cruce_uniforme(padre1, padre2)
            mutacion_uniforme(hijo1, prob_mutacion)
            mutacion_uniforme(hijo2, prob_mutacion)
            hijo1.evaluar(evaluacion_func, **kwargs)
            hijo2.evaluar(evaluacion_func, **kwargs)
            nueva_poblacion.extend([hijo1, hijo2])

        poblacion = nueva_poblacion

        # Estadísticas de la generación
        min_fitness, max_fitness, avg_fitness = calcular_estadisticas(poblacion)
        print(f"Generación {gen} - Min: {min_fitness} Max: {max_fitness} Avg: {avg_fitness}")

        # Visualizar la mejor solución en la generación actual
        mejor_actual = max(poblacion, key=lambda ind: ind.fitness)
        graficar_terreno(ax, mejor_actual, kwargs['radio_aspersor'], gen, kwargs['lado_terreno'], kwargs['tam_punto'], mejor_actual.fitness)
        plt.draw()
        plt.pause(0.5)  # Pausa para actualizar la gráfica

        # Detener si se ha cubierto todo el terreno
        if mejor_actual.fitness >= area_maxima:
            mejor_individuo = mejor_actual
            break

    if not mejor_individuo:
        mejor_individuo = max(poblacion, key=lambda ind: ind.fitness)

    plt.ioff()
    graficar_terreno(ax, mejor_individuo, kwargs['radio_aspersor'], num_generaciones, kwargs['lado_terreno'], kwargs['tam_punto'], mejor_individuo.fitness)
    plt.show()

    return mejor_individuo
