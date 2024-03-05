#Leer documento y dividirlo en paths: 
import pandas as pd
import os
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain.prompts.prompt import PromptTemplate

from pymongo import MongoClient


from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import DataFrameLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA

from chatbot_utils import load_dataset, create_chunks, create_or_get_vector_store,parse,insert_bbdd  # Importa las funciones desde utils.py
from chatbot_preprompts import system_message_prompt_info, system_message_prompt_pedido  # Importa las definiciones desde prompts.py

import os
import sys 
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from speech.speechRecognizer import SpeechRecognizer
from speech.textToSpeech import text_to_speech ,  reproducir_mp3


def calculate_retriever(vector_store,dataset):
     # Set 'k' value automatically as the number of lines in the dataset
    k_value = len(dataset)
    print(k_value)
  
    # 'as_retriever()' converts the vector store into a retriever object
    retriever1 = vector_store.as_retriever()
    retriever1.search_kwargs = {'k': k_value}  # NUMBER OF LINES OF CSV
    return retriever1

def get_conversation_chain(retriever1,system_message_prompt,query,memory):
    prompt = PromptTemplate(
        input_variables=["history", "context", "question"],
        template=system_message_prompt,
)

   
    retrieval_chain = RetrievalQA.from_chain_type(llm=ChatOpenAI(model="gpt-4-1106-preview", temperature=0.0),
                                              chain_type='stuff',
                                              retriever=retriever1,
                                              chain_type_kwargs={
                                                  "prompt": prompt,
                                                  "memory": memory
                                              })
    response = retrieval_chain(query)
    print(response['result'])
    return(response['result'])


def initMemoria():
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
    prompt=system_message_prompt_info


    while True:
        input("Press Enter to start recording...")  # Wait for keyboard input before recording
        speech_recognizer =SpeechRecognizer()
        query = speech_recognizer.insert_audio()
        print(query)

       
        #query=input("Introduce una petición al chatbot : ") #Para escribir la query manualmente

        # Si la pregunta del usuario es "Quiero empezar a pedir", cambiar el estado.
        if any(word in query.strip().lower() for word in ["quiero empezar a pedir", "deseo pedir", "ya quiero pedir","quiero pedir"]) and not any(word in query.strip().lower() for word in ["no"]):
            prompt=system_message_prompt_pedido
            response = get_conversation_chain(retriever1,prompt,query,memory)
                       

        else: response = get_conversation_chain(retriever1,prompt,query,memory)
        
        # Convertir la respuesta a voz y reproducir
        mp3_file = text_to_speech(response)
        reproducir_mp3(mp3_file)

        #Cuando imprima el ticket, lo subimos a la bbdd de tickets y se para 
        if "Número de pedido" in response:
            parseo=parse(response)
            insert_bbdd(parseo)
            sys.exit()

        #print(memory.load_memory_variables({})) #Para ver historico de la converacion 

   
   
if __name__ == "__main__":
    main()
