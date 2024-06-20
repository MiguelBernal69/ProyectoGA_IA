from flask import Flask, jsonify, render_template
from genetic_algorithm import inicializar_poblacion, algoritmo_genetico_paso_a_paso

app = Flask(__name__)
poblacion = inicializar_poblacion()
current_generation = 0  # Variable global para rastrear la generación actual

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['GET'])
def start_optimization():
    global poblacion, current_generation
    poblacion = inicializar_poblacion()  # Reinicia la población
    current_generation = 0  # Reinicia la generación
    return jsonify(poblacion=poblacion, current_generation=current_generation)

@app.route('/next_generation', methods=['GET'])
def next_generation():
    global poblacion, current_generation
    poblacion, finished = algoritmo_genetico_paso_a_paso(poblacion)
    return jsonify(poblacion=poblacion, current_generation=current_generation, finished=finished)

if __name__ == '__main__':
    app.run(debug=True)