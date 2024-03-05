from dotenv import load_dotenv
from langchain.prompts import (
    HumanMessagePromptTemplate,
)
import streamlit as st
from chatbot_utils import load_dataset, create_chunks, create_or_get_vector_store, get_conversation_chain,handle_style_and_responses  # Importa las funciones desde utils.py
from chatbot_preprompts import system_message_prompt_info, system_message_prompt_pedido  # Importa las definiciones desde prompts.py

import sys
sys.path.append("..")
from speech.speechRecognizer import SpeechRecognizer
from speech.textToSpeech import text_to_speech ,  reproducir_mp3


##ESTE FICHERO ES DE UN CHATBOT 100% funcional, que usa una interfaz web (streamlit). En el resultado final, no lo usaremos 


def initialize_session():
    if "vectorstore" not in st.session_state:
        st.session_state.vectorstore = None
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None


def main():
    load_dotenv() # load environment variables (API_KEY)
    df = load_dataset() # ARRIBA LO DEFINO
   
    chunks = create_chunks(df, 2000, 0) ##ARRIBA LO DEFINO 
    
    human_message_prompt = HumanMessagePromptTemplate.from_template("{question}")
    
    initialize_session()

    if st.session_state.vectorstore is None:
        st.session_state.vectorstore = create_or_get_vector_store(chunks) #base de datos del menu 
    
    
 
        
    st.set_page_config(
        page_title="Chatbot del Menú del Restaurante",
        page_icon=":fork_and_knife:",
    )

    st.title("Chatbot del Menú del Restaurante")
    st.subheader("Chatea con el chatbot para obtener información sobre el menú del restaurante.")

    st.image("https://images.unsplash.com/photo-1485827404703-89b55fcc595e") 

    # Pregunta predeterminada para iniciar la conversación
    first_question = "Buenos días. "
    user_question = st.text_input("Ask your question", first_question)
    

   #Graba la voz del usuario
    if st.button("Start Voice Recognition"):
        speech_recognizer =SpeechRecognizer()
        user_question = speech_recognizer.insert_audio()
   


#Mode "Info" predetermindado    
    if "prompt_mode" not in st.session_state:
        st.session_state.prompt_mode = "info"

    # Si la pregunta del usuario es "Quiero empezar a pedir", cambiar el estado.
    if any(word in user_question.strip().lower() for word in ["quiero empezar a pedir", "deseo pedir", "ya quiero pedir","quiero pedir"]) and not any(word in user_question.strip().lower() for word in ["no"]):

   # if "quiero empezar a pedir" in user_question.strip().lower() or "deseo pedir" in user_question.strip().lower() or "ya quiero pedir" in user_question.strip().lower():
        st.session_state.prompt_mode = "pedido"
        # Responder al usuario informándole que puede empezar a pedir.

        st.write("Perfecto. ¿Qué deseas pedir?.")
        
        # Convertir la respuesta a voz y reproducir
        mp3_file = text_to_speech("Perfecto. ¿Qué deseas pedir?")
        reproducir_mp3(mp3_file)
        # No procesar esta pregunta en el chatbot.
        user_question = ""


    # Elige el prompt correcto dependiendo del estado.
    if st.session_state.prompt_mode == "info":
        system_message_prompt = system_message_prompt_info
    else:
        system_message_prompt = system_message_prompt_pedido
    
    st.session_state.conversation = get_conversation_chain(
        st.session_state.vectorstore, system_message_prompt, human_message_prompt
    )

    with st.spinner("Processing..."):
           if user_question:
                response = handle_style_and_responses(user_question)
                
                
               
                # Mostrar la respuesta en texto
                st.write("Chatbot:", response)
               

                #PASAR DE TEXTO A VOZ EL SPEECH DEL USUARIO 
                last_message = st.session_state.chat_history[-1]  #content='¡Buenos días! Bienvenido a nuestro restaurante. ¿Desea pedir algo o necesita información sobre nuestro menú?'
                last_message_content = last_message.content            #'¡Buenos días! Bienvenido a nuestro restaurante. ¿Desea pedir algo o necesita información sobre nuestro menú?'


                # Convertir la respuesta a voz y reproducir
                mp3_file = text_to_speech(last_message_content)
                reproducir_mp3(mp3_file)
                
 
   
if __name__ == "__main__":
    main()



