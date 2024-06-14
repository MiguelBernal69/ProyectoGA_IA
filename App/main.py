import matplotlib.pyplot as plt
import random
from deap import base, creator, tools, algorithms
from elements.Terreno import Terreno
from elements.Aspersor import Aspersor

# Parámetros
LADO_TERRENO = 100  # Lado del terreno (cuadrado)
NUM_ASPERSORES = 10  # Número de aspersores
RADIO_ASPERSOR = 15  # Radio de cada aspersor
POBLACION_INICIAL = 50
GENERACIONES = 20

# Configuración del algoritmo genético
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("attr_float", random.uniform, 0, LADO_TERRENO)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=2*NUM_ASPERSORES)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evaluar_individuo(individuo, lado_terreno, radio_aspersor):
    terreno = Terreno(lado_terreno)
    for i in range(0, len(individuo), 2):
        aspersor = Aspersor(individuo[i], individuo[i + 1], radio_aspersor)
        terreno.agregar_aspersor(aspersor)
    return (terreno.area_cubierta(),)

toolbox.register("evaluate", evaluar_individuo, lado_terreno=LADO_TERRENO, radio_aspersor=RADIO_ASPERSOR)
toolbox.register("mate", tools.cxBlend, alpha=0.5)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=10, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=3)

def graficar_terreno(ax, individuo, radio_aspersor, iteracion):
    ax.clear()
    ax.set_aspect('equal')
    plt.xlim(0, LADO_TERRENO)
    plt.ylim(0, LADO_TERRENO)

    # Dibujar el terreno
    terreno = plt.Rectangle((0, 0), LADO_TERRENO, LADO_TERRENO, fill=None, edgecolor='r')
    ax.add_patch(terreno)

    # Dibujar los aspersores
    aspersores = [Aspersor(individuo[i], individuo[i + 1], radio_aspersor) for i in range(0, len(individuo), 2)]
    for aspersor in aspersores:
        circle = plt.Circle((aspersor.x, aspersor.y), radio_aspersor, fill=True, edgecolor='b', alpha=0.5)
        ax.add_patch(circle)
    
    # Mostrar el número de iteración
    ax.text(0.95, 0.05, f'Iteración: {iteracion}', horizontalalignment='right', verticalalignment='center', transform=ax.transAxes, fontsize=12, bbox=dict(facecolor='white', alpha=0.5))

def main():
    random.seed(42)
    pop = toolbox.population(n=POBLACION_INICIAL)

    # Estadísticas
    stats = tools.Statistics(lambda ind: ind.fitness.values[0])
    stats.register("avg", lambda x: sum(x) / len(x))
    stats.register("min", min)
    stats.register("max", max)

    # Configuración de la gráfica
    fig, ax = plt.subplots()
    plt.ion()
    plt.show()

    # Algoritmo genético
    for gen in range(GENERACIONES):
        # Selección
        offspring = toolbox.select(pop, len(pop))
        offspring = list(map(toolbox.clone, offspring))

        # Cruza y mutación
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < 0.5:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < 0.2:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Evaluar individuos con fitness no calculado
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # Reemplazar la población con los descendientes
        pop[:] = offspring

        # Estadísticas de la generación
        record = stats.compile(pop) if stats else {}
        print(f"Generación {gen} - {record}")

        # Visualizar la mejor solución en la generación actual
        best_ind = tools.selBest(pop, 1)[0]
        graficar_terreno(ax, best_ind, RADIO_ASPERSOR, gen)
        plt.draw()
        plt.pause(0.5)  # Pausa para actualizar la gráfica

    # Mostrar la mejor solución final
    best_ind = tools.selBest(pop, 1)[0]
    print(f"Mejor individuo: {best_ind}")
    print(f"Fitness: {best_ind.fitness.values[0]}")

    # Visualización final
    plt.ioff()
    graficar_terreno(ax, best_ind, RADIO_ASPERSOR, GENERACIONES)
    plt.show()

if __name__ == "__main__":
    main()
