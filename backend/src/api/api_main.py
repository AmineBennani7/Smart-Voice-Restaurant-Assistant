from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS


import os
import sys 

sys.path.insert(0, 'backend/src/chatbot')

from  chatbot_utils import load_dataset, create_chunks, create_or_get_vector_store, parse, insert_bbdd, calculate_retriever, get_conversation_chain 
from  chatbot_preprompts import system_message_prompt_info, system_message_prompt_pedido
from  chatbot_main import initMemoria


app = Flask(__name__)
CORS(app)





# Inicializar variables globales
load_dotenv()  # Carga las variables de entorno
dataset = load_dataset("menu_dataset/menus_dataset.csv")
chunks = create_chunks(dataset, 2000, 0)
vector_store = create_or_get_vector_store(chunks)
retriever = calculate_retriever(vector_store, dataset)


...
memory = initMemoria()  # Ponemos la inicialización fuera de la función del enrutador
prompt = system_message_prompt_info

...

#SOLICITUD POST teniendo en cuenta el historial de la conversacion (una vez el programa flask apagado, se borra el historial y reinicializa todo)
@app.route("/chat", methods=["POST"])
def chat_with_history(): 
    global memory, prompt  # Declaramos que vamos a utilizar las variables globales "memory" y "prompt"
    data = request.get_json()
    user_question = data['user_question']

    # Si la pregunta del usuario es "Quiero empezar a pedir", cambiar el estado.
    if any(word in user_question.strip().lower() for word in ["quiero empezar a pedir", "deseo pedir", "ya quiero pedir","quiero pedir"]) and not any(word in user_question.strip().lower() for word in ["no"]):
        prompt = system_message_prompt_pedido

    try:
        response = get_conversation_chain(retriever, prompt, user_question, memory)    
    except Exception as e:
        return jsonify({'error': str(e)}), 500  

    chat_history = [{'message': message.content, 'type': type(message).__name__} for message in memory.chat_memory.messages]
    return jsonify({"response": response, "chat_history": chat_history})

if __name__ == '__main__':
    app.run(debug=True, port=8000)




