import os
from dotenv import load_dotenv
from langchain.memory import ConversationBufferMemory
from chatbot_utils import load_dataset, create_chunks, create_or_get_vector_store,parse,insert_bbdd,calculate_retriever,get_conversation_chain  # Importa las funciones desde utils.py
from chatbot_preprompts import system_message_prompt_info, system_message_prompt_pedido  # Importa las definiciones desde prompts.py
import os
import sys 
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from speech.speechRecognizer import SpeechRecognizer
from speech.textToSpeech import text_to_speech ,  reproducir_mp3





def initMemoria(): #input_key='question'
    memory = ConversationBufferMemory(
    memory_key="history",
    input_key="question"
)
    return memory

  
def main():
    
    load_dotenv()  # load environment variables (API_KEY)
    dataset = load_dataset("menu_dataset/menus_dataset.csv")
    chunks = create_chunks(dataset, 2000, 0)
  
    # Create or load the vector store, calculate retriever, init memory and defaultPrompt
    vector_store = create_or_get_vector_store(chunks)
    retriever1=calculate_retriever(vector_store,dataset)
    memory=initMemoria()
    print(memory)
    prompt=system_message_prompt_info #Default prompt


    while True:
        input("Press Enter to start recording...") 
        speech_recognizer =SpeechRecognizer()
        query = speech_recognizer.insert_audio()
        print(query)
       
        #query=input("Introduce una petición al chatbot : ") #Para escribir la query manualmente

        # Si la pregunta del usuario es "Quiero empezar a pedir", cambiar el estado.
        if any(word in query.strip().lower() for word in ["quiero empezar a pedir", "deseo pedir", "ya quiero pedir","quiero pedir"]) and not any(word in query.strip().lower() for word in ["no"]):
            prompt=system_message_prompt_pedido
            response = get_conversation_chain(retriever1,prompt,query,memory)
                       

        else: 
            response = get_conversation_chain(retriever1,prompt,query,memory)
        
        # Convertir la respuesta a voz y reproducir
        mp3_file = text_to_speech(response)
        reproducir_mp3(mp3_file)

        #Cuando imprima el ticket, lo subimos a la bbdd de tickets y acabamos el sistema  
        if "Número de pedido" in response:
            parseo=parse(response)
            insert_bbdd(parseo)
            sys.exit()


       # print(memory) #chat_memory=ChatMessageHistory(messages=[HumanMessage(content='buenas tardes'), AIMessage(content='¡Bienvenidos a nuestro restaurante! ¿Desean hacer un pedido o quieren información sobre nuestro menú?')]) input_key='question'
        #print(memory.load_memory_variables({})) #Para ver historialde la converacion 
       #{'history': 'Human: hola\n
            #AI: Bienvenido a nuestro restaurante. ¿Desea hacer un pedido o quiere información sobre nuestro menú?\n
            #Human: qué hay en el menú\
            #nAI: En nuestro menú tenemos las siguientes categorías: Pizzas, Calzones, Pastas y Bebidas. ¿Desea más detalles sobre alguna categoría en particular?'}

   
if __name__ == "__main__":
    main()
