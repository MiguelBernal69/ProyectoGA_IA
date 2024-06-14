import random

class Individuo:
    def __init__(self, genes):
        self.genes = genes
        self.fitness = None
    
    def evaluar(self, evaluacion_func, *args, **kwargs):
        self.fitness = evaluacion_func(self.genes, *args, **kwargs)
    
    def mutar(self, mutacion_func, prob_mutacion, *args, **kwargs):
        if random.random() < prob_mutacion:
            self.genes = mutacion_func(self.genes, *args, **kwargs)

def inicializar_poblacion(tam_poblacion, longitud_gen):
    return [Individuo([random.uniform(0, 100) for _ in range(longitud_gen)]) for _ in range(tam_poblacion)]

def seleccion_torneo(poblacion, num_seleccionados, torneo_size):
    seleccionados = []
    for _ in range(num_seleccionados):
        concursantes = random.sample(poblacion, torneo_size)
        seleccionado = max(concursantes, key=lambda x: x.fitness)
        seleccionados.append(seleccionado)
    return seleccionados

def cruce_uniforme(padre1, padre2):
    genes_hijo1 = []
    genes_hijo2 = []
    for gen1, gen2 in zip(padre1.genes, padre2.genes):
        if random.random() < 0.5:
            genes_hijo1.append(gen1)
            genes_hijo2.append(gen2)
        else:
            genes_hijo1.append(gen2)
            genes_hijo2.append(gen1)
    return Individuo(genes_hijo1), Individuo(genes_hijo2)

def mutacion_uniforme(genes, prob_mutacion, rango_gen):
    return [gen + random.uniform(-rango_gen, rango_gen) if random.random() < prob_mutacion else gen for gen in genes]


def algoritmo_genetico(tam_poblacion, longitud_gen, num_generaciones, prob_mutacion, evaluacion_func, *args, **kwargs):
    poblacion = inicializar_poblacion(tam_poblacion, longitud_gen)
    
    for ind in poblacion:
        ind.evaluar(evaluacion_func, *args, **kwargs)
    
    mejor_individuo = max(poblacion, key=lambda x: x.fitness)
    mejor_fitness = mejor_individuo.fitness
    
    for gen in range(num_generaciones):
        seleccionados = seleccion_torneo(poblacion, tam_poblacion, 3)
        descendientes = []
        
        while len(descendientes) < tam_poblacion:
            padre1, padre2 = random.sample(seleccionados, 2)
            hijo1, hijo2 = cruce_uniforme(padre1, padre2)
            hijo1.mutar(mutacion_uniforme, prob_mutacion, 10)
            hijo2.mutar(mutacion_uniforme, prob_mutacion, 10)
            descendientes.extend([hijo1, hijo2])
        
        poblacion = descendientes
        
        for ind in poblacion:
            ind.evaluar(evaluacion_func, *args, **kwargs)
        
        mejor_individuo = max(poblacion, key=lambda x: x.fitness)
        mejor_fitness = max(mejor_fitness, mejor_individuo.fitness)
        
        print(f"Generación {gen}: Mejor Fitness = {mejor_fitness}")
    
    return mejor_individuo

def evaluar_terreno(genes, lado_terreno, radio_aspersor):
    terreno = Terreno(lado_terreno)
    for i in range(0, len(genes), 2):
        aspersor = Aspersor(genes[i], genes[i + 1], radio_aspersor)
        terreno.agregar_aspersor(aspersor)
    return terreno.area_cubierta()

if __name__ == "__main__":
    tam_poblacion = 50
    longitud_gen = 2 * NUM_ASPERSORES
    num_generaciones = 20
    prob_mutacion = 0.2
    
    mejor_individuo = algoritmo_genetico(tam_poblacion, longitud_gen, num_generaciones, prob_mutacion, evaluar_terreno, LADO_TERRENO, RADIO_ASPERSOR)
    
    print(f"Mejor individuo: {mejor_individuo.genes}")
    print(f"Fitness: {mejor_individuo.fitness}")
