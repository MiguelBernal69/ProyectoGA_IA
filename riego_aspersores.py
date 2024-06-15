import numpy as np

# Dimensiones del área de riego
rows = 20
cols = 20

# Necesidades de agua por celda (litros)
water_needs = np.random.uniform(5, 15, size=(rows, cols))

class Sprinkler:
    def __init__(self, x, y, radius, flow_rate):
        self.x = x
        self.y = y
        self.radius = radius
        self.flow_rate = flow_rate

    def water_distribution(self, area):
        distribution = np.zeros(area.shape)
        for i in range(area.shape[0]):
            for j in range(area.shape[1]):
                distance = np.sqrt((i - self.x)**2 + (j - self.y)**2)
                if distance <= self.radius:
                    distribution[i, j] += self.flow_rate * (1 - distance / self.radius)
        return distribution

def fitness(sprinklers, water_needs):
    area = np.zeros(water_needs.shape)
    for sprinkler in sprinklers:
        area += sprinkler.water_distribution(water_needs)

    mismatch = np.abs(area - water_needs)
    total_water_used = np.sum(area)

    fitness_value = np.sum(mismatch) + total_water_used
    return -fitness_value

def create_initial_population(pop_size, num_sprinklers, rows, cols):
    population = []
    for _ in range(pop_size):
        sprinklers = []
        for _ in range(num_sprinklers):
            x = np.random.randint(0, rows)
            y = np.random.randint(0, cols)
            radius = np.random.uniform(1, 5)
            flow_rate = np.random.uniform(0.1, 1.0)
            sprinklers.append(Sprinkler(x, y, radius, flow_rate))
        population.append(sprinklers)
    return population

def selection(population, fitness_values, k=3):
    selected = []
    for _ in range(len(population)):
        tournament_indices = np.random.choice(len(population), k)
        tournament_fitness = [fitness_values[i] for i in tournament_indices]
        winner_index = tournament_indices[np.argmax(tournament_fitness)]
        selected.append(population[winner_index])
    return selected

def crossover(parent1, parent2):
    child1, child2 = [], []
    for i in range(len(parent1)):
        if np.random.rand() < 0.5:
            child1.append(parent1[i])
            child2.append(parent2[i])
        else:
            child1.append(parent2[i])
            child2.append(parent1[i])
    return child1, child2

def mutate(sprinkler, mutation_rate=0.05):
    if np.random.rand() < mutation_rate:
        sprinkler.x = np.random.randint(0, rows)
    if np.random.rand() < mutation_rate:
        sprinkler.y = np.random.randint(0, cols)
    if np.random.rand() < mutation_rate:
        sprinkler.radius = np.random.uniform(1, 5)
    if np.random.rand() < mutation_rate:
        sprinkler.flow_rate = np.random.uniform(0.1, 1.0)

def genetic_algorithm(pop_size, num_sprinklers, rows, cols, generations, mutation_rate=0.01):
    population = create_initial_population(pop_size, num_sprinklers, rows, cols)
    for generation in range(generations):
        fitness_values = [fitness(ind, water_needs) for ind in population]
        print(f"Generación {generation}: Mejor fitness = {max(fitness_values)}")

        selected_population = selection(population, fitness_values)
        next_generation = []
        for i in range(0, len(selected_population), 2):
            if i + 1 < len(selected_population):
                parent1, parent2 = selected_population[i], selected_population[i+1]
                child1, child2 = crossover(parent1, parent2)
                next_generation.extend([child1, child2])
            else:
                next_generation.append(selected_population[i])

        population = next_generation
        for individual in population:
            for sprinkler in individual:
                mutate(sprinkler, mutation_rate)

    best_individual = population[np.argmax([fitness(ind, water_needs) for ind in population])]
    return best_individual

# Parámetros del algoritmo genético
pop_size = 100
num_sprinklers = 5
generations = 100

# Ejecutar el algoritmo
best_configuration = genetic_algorithm(pop_size, num_sprinklers, rows, cols, generations)

# Mostrar la mejor configuración encontrada
for sprinkler in best_configuration:
    print(f"Aspersor en ({sprinkler.x}, {sprinkler.y}) con radio {sprinkler.radius} y tasa de flujo {sprinkler.flow_rate}")
