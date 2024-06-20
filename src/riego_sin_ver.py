import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon
from shapely.ops import unary_union
import numpy as np
import random
import datetime

def obtener_datos():
    base = float(input("Ingrese la base del área a regar: "))
    altura = float(input("Ingrese la altura del área a regar: "))
    cantidad_aspersores = int(input("Ingrese la cantidad de aspersores: "))
    radio_aspersor = float(input("Ingrese el radio de los aspersores: "))
    
    print("Seleccione el departamento en la que desea instalar los aspersores:")
    print(" (1) Andina (La Paz - Oruro - Potosi)")
    print(" (2) Subandina (Cochabamba - Chuquisaca - Tarija)")
    print(" (3) De Llanos (Pando - Beni - Santa Cruz)")

    zona = int(input("Seleccione la zona (1-3): "))
    if zona == 1:
        print(" (1) La Paz")
        print(" (2) Oruro")
        print(" (3) Potosí")
        depto_opcion = int(input("Seleccione el departamento (1-3): "))
        if depto_opcion == 1:
            departamento = "La Paz"
        elif depto_opcion == 2:
            departamento = "Oruro"
        elif depto_opcion == 3:
            departamento = "Potosí"
    elif zona == 2:
        print(" (1) Cochabamba")
        print(" (2) Chuquisaca")
        print(" (3) Tarija")
        depto_opcion = int(input("Seleccione el departamento (1-3): "))
        if depto_opcion == 1:
            departamento = "Cochabamba"
        elif depto_opcion == 2:
            departamento = "Chuquisaca"
        elif depto_opcion == 3:
            departamento = "Tarija"
    elif zona == 3:
        print(" (1) Pando")
        print(" (2) Beni")
        print(" (3) Santa Cruz")
        depto_opcion = int(input("Seleccione el departamento (1-3): "))
        if depto_opcion == 1:
            departamento = "Pando"
        elif depto_opcion == 2:
            departamento = "Beni"
        elif depto_opcion == 3:
            departamento = "Santa Cruz"
    
    return base, altura, cantidad_aspersores, radio_aspersor, departamento

def inicializar_poblacion(cantidad_aspersores, base, altura, tamano_poblacion):
    return np.array([[np.random.uniform(0, base), np.random.uniform(0, altura)] for _ in range(tamano_poblacion * cantidad_aspersores)]).reshape(tamano_poblacion, cantidad_aspersores, 2)

def calcular_fitness(individuo, radio, area_total):
    circulos = [Point(x, y).buffer(radio) for x, y in individuo]
    area_cubierta = unary_union(circulos)
    area_regada = area_cubierta.intersection(area_total).area
    area_no_cubierta = area_total.area - area_regada
    fitness = area_regada - area_no_cubierta
    return max(fitness, 0), area_regada / area_total.area * 100

def seleccion(poblacion, fitnesses):
    total_fitness = sum(fitnesses)
    if total_fitness == 0:
        total_fitness = 1  # Evitar división por cero
    probs = [f / total_fitness for f in fitnesses]
    probs = np.array(probs)
    if probs.sum() == 0:
        probs = np.ones_like(probs) / len(probs)  # Asignar probabilidades uniformes si la suma es 0
    else:
        probs /= probs.sum()  # Asegurar que las probabilidades sumen 1
    indices = np.random.choice(len(poblacion), size=len(poblacion), replace=True, p=probs)
    return poblacion[indices]

def cruzamiento(padre1, padre2):
    punto_cruce = np.random.randint(1, len(padre1))
    hijo = np.vstack((padre1[:punto_cruce], padre2[punto_cruce:]))
    return hijo

def mutacion(individuo, base, altura):
    if np.random.rand() < 0.2:  # Incrementar probabilidad de mutación al 20%
        indice = np.random.randint(len(individuo))
        individuo[indice] = [np.random.uniform(0, base), np.random.uniform(0, altura)]
    return individuo

def algoritmo_genetico(base, altura, cantidad_aspersores, radio, generaciones, umbral_porcentaje, tamano_poblacion):
    poblacion = inicializar_poblacion(cantidad_aspersores, base, altura, tamano_poblacion)
    area_total = Polygon([(0, 0), (base, 0), (base, altura), (0, altura)])
    
    # Visualizar la población inicial
    visualizar_generacion(poblacion[0], radio, base, altura, area_total, "Inicial", 0)
    
    mejor_fitness_global = -np.inf
    mejor_individuo_global = None
    
    for generacion in range(generaciones):
        fitnesses, porcentajes_regados = zip(*[calcular_fitness(individuo, radio, area_total) for individuo in poblacion])
        
        # Elitismo: conservar el mejor individuo
        mejor_fitness_generacion = max(fitnesses)
        mejor_individuo_generacion = poblacion[np.argmax(fitnesses)]
        
        if mejor_fitness_generacion > mejor_fitness_global:
            mejor_fitness_global = mejor_fitness_generacion
            mejor_individuo_global = mejor_individuo_generacion
        
        poblacion = seleccion(poblacion, fitnesses)
        
        nueva_poblacion = [mejor_individuo_generacion]  # Preservar el mejor individuo actual
        for i in range(0, len(poblacion) - 1, 2):
            if i+1 < len(poblacion):
                hijo1 = cruzamiento(poblacion[i], poblacion[i+1])
                hijo2 = cruzamiento(poblacion[i+1], poblacion[i])
                nueva_poblacion.append(mutacion(hijo1, base, altura))
                nueva_poblacion.append(mutacion(hijo2, base, altura))
        
        poblacion = np.array(nueva_poblacion)
        mejor_porcentaje = max(porcentajes_regados)
        
        #print("------------------------------------------")
        print(f"Generación {generacion+1}: {mejor_porcentaje:.2f}% cubierto.")
        #print("------------------------------------------")
        #print(f"Coordenadas de aspersores: \n{mejor_individuo_generacion}")
        #print("------------------------------------------")
        
        if mejor_porcentaje >= umbral_porcentaje:
            print(f"Umbral de cobertura alcanzado en la generación {generacion+1}.")
            break
        
    return mejor_individuo_global, mejor_porcentaje

def visualizar_generacion(poblacion, radio, base, altura, area_total, generacion, porcentaje_regado):
    circulos = [Point(x, y).buffer(radio) for x, y in poblacion]
    area_cubierta = unary_union(circulos)
    
    fig, ax = plt.subplots()


    x, y = area_total.exterior.xy
    ax.plot(x, y, color='blue', alpha=0.5, linewidth=3, solid_capstyle='round', zorder=2)
    
    if area_cubierta.geom_type == 'Polygon':
        x, y = area_cubierta.exterior.xy
        ax.fill(x, y, alpha=0.5, fc='lightblue', ec='lightblue')
        #ax.fill(x, y, alpha=0.5, fc='lightblue', ec='lightblue', label='Área cubierta')
    elif area_cubierta.geom_type == 'MultiPolygon':
        for polygon in area_cubierta.geoms:
            x, y = polygon.exterior.xy
            ax.fill(x, y, alpha=0.5, fc='lightblue', ec='lightblue')
            #ax.fill(x, y, alpha=0.5, fc='lightblue', ec='lightblue', label='Área cubierta')
    
    x, y = poblacion[:,0], poblacion[:,1]
    ax.plot(x, y, 'o', color='red')
    
    ax.set_xlim(0, base)
    ax.set_ylim(0, altura)
    ax.set_xticks(np.arange(0, base+1, 5))
    ax.set_yticks(np.arange(0, altura+1, 5))
    ax.set_aspect('equal', 'box')
    ax.grid(True)
    ax.set_title(f'Generación {generacion} - {porcentaje_regado:.2f}% cubierto.')
    ax.legend()
    plt.show()

def generar_valores_sensores(departamento):
    humedad_tierra = random.uniform(0, 100) #Valores de humedad de tierra generado.
    temperatura_ambiente = random.uniform(0, 100) #Valores de temperatura de tierra generado.
    return humedad_tierra, temperatura_ambiente

def evaluar_riego(departamento, humedad_tierra, temperatura_ambiente):
    parametros = {
        "La Paz": {"min_humedad": 40, "max_humedad": 80, "rango_temp": (10, 25)},
        "Oruro": {"min_humedad": 30, "max_humedad": 70, "rango_temp": (10, 20)},
        "Potosí": {"min_humedad": 30, "max_humedad": 70, "rango_temp": (10, 20)},
        "Cochabamba": {"min_humedad": 50, "max_humedad": 85, "rango_temp": (15, 25)},
        "Chuquisaca": {"min_humedad": 50, "max_humedad": 85, "rango_temp": (15, 25)},
        "Tarija": {"min_humedad": 50, "max_humedad": 85, "rango_temp": (15, 30)},
        "Pando": {"min_humedad": 60, "max_humedad": 90, "rango_temp": (20, 35)},
        "Beni": {"min_humedad": 60, "max_humedad": 90, "rango_temp": (20, 30)},
        "Santa Cruz": {"min_humedad": 50, "max_humedad": 85, "rango_temp": (20, 35)},
    }
    
    if departamento in parametros:
        param = parametros[departamento]
        min_humedad = param["min_humedad"]
        max_humedad = param["max_humedad"]
        rango_temp_baja, rango_temp_alta = param["rango_temp"]
        
        if humedad_tierra < min_humedad:
            if temperatura_ambiente < rango_temp_baja:
                return "Regar pero no mucho"
            elif temperatura_ambiente > rango_temp_alta:
                return "Regar un poco más de lo normal"
            else:
                return "Regar normalmente"
        elif humedad_tierra > max_humedad:
            return "No regar, humedad excesiva"
        else:
            return "No regar, humedad adecuada"
    else:
        return "Departamento no reconocido"

def generar_litros_disponibles():
    return random.uniform(500, 10000)  # Simulación de litros disponibles

def calcular_litros_usados(departamento, cantidad_aspersores):
    tiempo_riego = {
        "La Paz": random.uniform(30, 60),
        "Oruro": random.uniform(30, 60),
        "Potosí": random.uniform(30, 60),
        "Cochabamba": random.uniform(20, 40),
        "Chuquisaca": random.uniform(20, 40),
        "Tarija": random.uniform(20, 40),
        "Pando": random.uniform(30, 60),
        "Beni": random.uniform(30, 60),
        "Santa Cruz": random.uniform(30, 60),
    }
    consumo_por_aspersor = 10  # Consumo promedio en litros por minuto
    tiempo = tiempo_riego[departamento]
    litros_usados = cantidad_aspersores * consumo_por_aspersor * tiempo
    return litros_usados, tiempo

def main():
    base, altura, cantidad_aspersores, radio, departamento = obtener_datos()
    ultima_poblacion, mejor_porcentaje = algoritmo_genetico(base, altura, cantidad_aspersores, radio, generaciones=500, umbral_porcentaje=95.0, tamano_poblacion=20)
    print("------------------------------------------")
    print(f"Optimización finalizada. Mejor cobertura: {mejor_porcentaje:.2f}%")
    print("------------------------------------------")
    print(f"Coordenadas finales de aspersores: \n{ultima_poblacion}")
    print("------------------------------------------")
    visualizar_generacion(ultima_poblacion, radio, base, altura, Polygon([(0, 0), (base, 0), (base, altura), (0, altura)]), "Final", mejor_porcentaje)
    
    # Generar valores de sensores
    humedad_tierra, temperatura_ambiente = generar_valores_sensores(departamento)
    print("\n------------------------------------------")
    print("Registro de Sensores:")
    print("------------------------------------------")
    print(f"{datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print(f"Humedad tierra: {humedad_tierra:.2f}%")
    print(f"Temperatura ambiente: {temperatura_ambiente:.2f} C°")
    
    # Evaluar riego
    accion_riego = evaluar_riego(departamento, humedad_tierra, temperatura_ambiente)
    print(f"Acción de riego: {accion_riego}")

    # Simulación de litros de agua disponibles
    litros_disponibles = generar_litros_disponibles()
    print("\n------------------------------------------")
    print(f"Litros disponibles: {litros_disponibles:.2f} litros")
    print("------------------------------------------")
    
    if "Regar" in accion_riego:
        litros_usados, tiempo_riego = calcular_litros_usados(departamento, cantidad_aspersores)
        print(f"Tiempo de riego: {tiempo_riego:.2f} minutos")
        print(f"Litros usados: {litros_usados:.2f} litros")

        if litros_usados > litros_disponibles:
            print("Advertencia: No hay suficiente agua disponible para el riego requerido.")
        else:
            print("Riego realizado correctamente.")
    else:
        print("No es necesario realizar riego.")

    print("------------------------------------------")

if __name__ == "__main__":
    main()