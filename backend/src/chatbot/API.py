from flask import Flask, request, jsonify
from chatbot_utils import *

app = Flask(__name__)

@app.route('/preguntar', methods=['POST'])  
def preguntar():
    # Asegurarse de que el request contenga JSON
    if not request.json or 'pregunta' not in request.json:
        return jsonify({'error': 'El cuerpo de la solicitud debe ser JSON y contener una pregunta'}), 400

    pregunta = request.json['pregunta']
    
    # Llamar a la función que maneja la lógica de tu chatbot. Asegúrate de ajustar esta llamada
    # a la función real y su implementación.
    try:
        # Suponiendo que `handle_style_and_responses` devuelva directamente la respuesta
        # del chatbot en forma de texto. Ajusta según sea necesario para tu implementación.
        respuesta = handle_style_and_responses(pregunta)
    except Exception as e:
        # Manejo de errores en caso de que algo falle al obtener la respuesta
        return jsonify({'error': str(e)}), 500

    # Devolver la respuesta en formato JSON
    return jsonify({'respuesta': respuesta})

if __name__=='__main__':
    app.run()