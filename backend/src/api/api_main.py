# Primero, crearemos el archivo api.py para la API Flask y definiremos un endpoint para recibir preguntas del usuario y 
#devolver respuestas del chatbot. Luego, integraremos esto en tu aplicación de Streamlit.
from flask import Flask, request, jsonify
import sys
sys.path.append("..")
from chatbot.chatbot_utils import  handle_style_and_responses

app_flask = Flask(__name__)

@app_flask.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()

    if 'question' not in data:
        return jsonify({"error": "Pregunta no proporcionada"}), 400

    user_question = data['question']
    response = handle_style_and_responses(user_question)

    return jsonify({"response": response})

def start_flask_app_in_thread():
    app_flask.run(port=8888)

if __name__ == '__main__':
    start_flask_app_in_thread()