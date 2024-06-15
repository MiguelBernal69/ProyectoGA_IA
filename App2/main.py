# main.py

from algoritmo_genetico import algoritmo_genetico, evaluar_terreno

if __name__ == "__main__":
    tam_poblacion = 50
    longitud_gen = 10  # 10 aspersores (x, y) => 10 * 2
    num_generaciones = 20
    prob_mutacion = 0.2
    lado_terreno = 100
    tam_punto = 5
    radio_aspersor = 10

    mejor_individuo = algoritmo_genetico(tam_poblacion, longitud_gen, num_generaciones, prob_mutacion, evaluar_terreno, lado_terreno=lado_terreno, tam_punto=tam_punto, radio_aspersor=radio_aspersor)
    print("Mejor individuo encontrado:")
    print(mejor_individuo.genes)
    print(f"Fitness: {mejor_individuo.fitness}")
