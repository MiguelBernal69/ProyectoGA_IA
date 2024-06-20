import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import seaborn as sns

# Parámetros del jardín
area_total = 50  # área ajustada para visualización
numero_aspersores = 10
cantidad_agua_total = 100  # en litros

# Inicializar población
def inicializar_poblacion(tamaño_poblacion, numero_aspersores, area_max):
    return [np.array([(
        random.uniform(0, area_max),  # x
        random.uniform(0, area_max),  # y
        random.uniform(1, 10),  # radio de cobertura
        random.uniform(1, 10)  # cantidad de agua
    ) for _ in range(numero_aspersores)]) for _ in range(tamaño_poblacion)]

# Función de aptitud
def calcular_aptitud(individuo):
    area_regada = sum(np.pi * aspersor[2]**2 for aspersor in individuo)
    agua_utilizada = sum(aspersor[3] for aspersor in individuo)
    if agua_utilizada > cantidad_agua_total:
        return 0  # Penalizar individuos que exceden la cantidad de agua disponible
    return area_regada / agua_utilizada

# Selección
def seleccion_por_torneo(poblacion, k=3):
    seleccionados = []
    for _ in range(len(poblacion)):
        aspirantes = random.sample(poblacion, k)
        mejor = max(aspirantes, key=calcular_aptitud)
        seleccionados.append(mejor)
    return seleccionados

# Cruzamiento
def cruzamiento(padre1, padre2):
    punto = random.randint(1, len(padre1) - 1)
    hijo1 = np.concatenate((padre1[:punto], padre2[punto:]))
    hijo2 = np.concatenate((padre2[:punto], padre1[punto:]))
    return hijo1, hijo2

# Mutación
def mutar(individuo, tasa_mutacion=0.1):
    for aspersor in individuo:
        if random.random() < tasa_mutacion:
            aspersor[0] = random.uniform(0, area_total)  # x
            aspersor[1] = random.uniform(0, area_total)  # y
            aspersor[2] = random.uniform(1, 10)  # radio de cobertura
            aspersor[3] = random.uniform(1, 10)  # cantidad de agua

# Generación de nueva población
def nueva_generacion(poblacion, tasa_cruzamiento=0.7, tasa_mutacion=0.1):
    nueva_poblacion = []
    seleccionados = seleccion_por_torneo(poblacion)
    for i in range(0, len(seleccionados), 2):
        if random.random() < tasa_cruzamiento:
            hijo1, hijo2 = cruzamiento(seleccionados[i], seleccionados[i+1])
            mutar(hijo1, tasa_mutacion)
            mutar(hijo2, tasa_mutacion)
            nueva_poblacion.extend([hijo1, hijo2])
        else:
            nueva_poblacion.extend([seleccionados[i], seleccionados[i+1]])
    return nueva_poblacion

# Algoritmo genético
tamaño_poblacion = 200
generaciones = 5000

poblacion = inicializar_poblacion(tamaño_poblacion, numero_aspersores, area_total)

for generacion in range(generaciones):
    poblacion = nueva_generacion(poblacion)
    mejor_individuo = max(poblacion, key=calcular_aptitud)
    print(f"Generación {generacion+1}: Mejor aptitud = {calcular_aptitud(mejor_individuo)}")

mejor_configuracion = max(poblacion, key=calcular_aptitud)
print("Mejor configuración de aspersores:", mejor_configuracion)

# Visualización gráfica
fig, ax = plt.subplots()

# Crear datos para el mapa de calor
x = [aspersor[0] for aspersor in mejor_configuracion]
y = [aspersor[1] for aspersor in mejor_configuracion]

# Dibujar el área total
ax.set_xlim(0, area_total)
ax.set_ylim(0, area_total)

# Dibujar el mapa de calor
sns.kdeplot(x=x, y=y, fill=True, cmap="Blues", ax=ax, alpha=0.6)

# Dibujar cada aspersor
for aspersor in mejor_configuracion:
    x, y, radio, _ = aspersor
    circulo = patches.Circle((x, y), radio, linewidth=1, edgecolor='r', facecolor='none')
    ax.add_patch(circulo)
    plt.plot(x, y, 'bo')  # Marcar el centro del aspersor

# Añadir barra de color
cbar = plt.colorbar(ax.collections[0], ax=ax, orientation='vertical')
cbar.set_label('Densidad de Riego')

# Configurar el gráfico
ax.set_aspect('equal', 'box')
plt.xlabel('X (metros)')
plt.ylabel('Y (metros)')
plt.title('Distribución de Riego')
plt.grid(True)

# Mostrar el gráfico
plt.show()
