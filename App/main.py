from algoritmo_genetico import algoritmo_genetico, evaluar_terreno
from elements.Terreno import Terreno
from elements.Aspersor import Aspersor

# Parámetros específicos del problema
LADO_TERRENO = 100  # Lado del terreno (cuadrado)
NUM_ASPERSORES = 10  # Número de aspersores
RADIO_ASPERSOR = 15  # Radio de cada aspersor
POBLACION_INICIAL = 50
GENERACIONES = 20

if __name__ == "__main__":
    mejor_individuo = algoritmo_genetico(
        tam_poblacion=POBLACION_INICIAL,
        longitud_gen=2 * NUM_ASPERSORES,
        num_generaciones=GENERACIONES,
        prob_mutacion=0.2,
        evaluacion_func=evaluar_terreno,
        lado_terreno=LADO_TERRENO,
        radio_aspersor=RADIO_ASPERSOR
    )
    
    print(f"Mejor individuo: {mejor_individuo.genes}")
    print(f"Fitness: {mejor_individuo.fitness}")
