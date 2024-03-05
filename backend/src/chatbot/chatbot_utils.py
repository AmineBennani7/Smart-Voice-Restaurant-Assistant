#pip install --upgrade pip 
# pip install -U langchain-openai

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
import streamlit as st
import sys
import re
from pymongo import MongoClient

from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import DataFrameLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.prompts.prompt import PromptTemplate

#from notifTeams import enviar_notificacion_a_teams




def load_dataset(dataset_name="menu_dataset/menus_dataset.csv"):
    #cargar un conjunto de datos desde un archivo csv 
    current_dir = os.path.dirname(os.path.realpath(__file__))  ##cojo nuestra current dir
    file_path = os.path.join(current_dir, dataset_name) #lo uno con \dataset.csv

    df = pd.read_csv(file_path) ##leo el csv
    
    return df


def create_chunks(dataset: pd.DataFrame, chunk_size:int, chunk_overlap:int):
   """
   Crea "chunks" (fragmentos) de información a partir del conjunto de datos proporcionado.
   """
   chunks = DataFrameLoader(    ##tomará el contenido de la columna "name" como contenido principal de cada documento.
      dataset, 
      page_content_column="name",
      
  ).load_and_split(    #dividir el contenido en fragmentos de 1000 
      text_splitter=RecursiveCharacterTextSplitter(
          chunk_size=1000
      )
  )
    
    # agregar metadatos a los fragmentos para facilitar la recuperación.
    
   for chunk in chunks:
     # print (chunk)

     # Agregar metadata como:
     name = chunk.page_content 
    # print(name)
     category = chunk.metadata['category']
     description= chunk.metadata['description']
     variations = chunk.metadata['variations']
     
     # Agregar todo al contenido
     content = f"Name: {name} \nCategory: {category} \nDescription: {description} \nVariations: {variations}"   # nExtras: {extras}"
     
     chunk.page_content = content
     
   return chunks




def create_or_get_vector_store(chunks) -> FAISS:
    """Crea o carga BBDD vectorial de manera local"""

    embeddings = OpenAIEmbeddings() # USAMOS EL EMBEDDING DE OPENAI DE MOMENTO

    if not os.path.exists("./vectorialDB"):
        print("CREATING DB")
         # load data
        vectorstore = FAISS.from_documents(
                chunks, embeddings
            )
        vectorstore.save_local("./vectorialDB")

    else:
        print("LOADING DB")
        vectorstore = FAISS.load_local("./vectorialDB", embeddings)

    return vectorstore


def get_conversation_chain_for_streamlit(vector_store: FAISS, system_message:str, human_message:str) -> ConversationalRetrievalChain:
    """
    Crear una instancia de un vector store (almacén de vectores) utilizando el índice FAISS
    Esto se utiliza para recuperar documentos similares (vectores) durante la conversación
    
    """
  # Si no ponemos nada usamos llm GPT-3 boost
    llm = ChatOpenAI(model="gpt-4-1106-preview", temperature=0.0)  # Se puede intercambiar por cualquier modelo de lenguaje de código abierto

   
  

    memory_key = "chat_history"
    ##Inicializo 
    if "conversation_memory" not in st.session_state:
        st.session_state.conversation_memory = ConversationBufferMemory(memory_key=memory_key, return_messages=True)    

    memory = st.session_state.conversation_memory
    
    # Cargar el conjunto de datos
    dataset = load_dataset()

    # Establecer automáticamente el valor de 'k' como el número de líneas en el conjunto de datos
    k_value = len(dataset)
   

    #MODIFICAR LA K SI AÑADIMOS MAS DATOS EN EL CSV
    # 'as_retriever()' convierte el vector store en un objeto retriever (recuperador)
    retriever1=vector_store.as_retriever()
    retriever1.search_kwargs = {'k':k_value}  #NUMERO DE LINEAS DEL CSV
    
    # Crear una cadena de recuperación conversacional utilizando LangChain
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever1,
        memory=memory,
        combine_docs_chain_kwargs={
            "prompt": ChatPromptTemplate.from_messages(
                [
                    system_message,
                    human_message,
                ]
            ),
       
        },
       
    )
    
    # Devolver la cadena conversacional creada
    return conversation_chain

#Del ticket sacado, sacamos el numDePedido, los platos y el precio total para la BBDD
def parse(texto_ticket):
        # Expresiones regulares actualizadas para extraer información del ticket
    patron_numero_pedido = re.compile(r'--\s*Número\s*de\s*pedido\s*:\s*(\d+)')
    patron_items = re.compile(r'--(Plato|Bebida)\s+(\d+) : (.*?); Tamaño : (.*?); Precio : (.*?); Cantidad : (\d+)')
    patron_precio_total = re.compile(r'--\s*Precio\s*total\s*:\s*([-+]?\d*\.\d+|\d+)')

    # Extraer información del ticket
    numero_pedido = int(patron_numero_pedido.search(texto_ticket).group(1))
    items_matches = patron_items.findall(texto_ticket)
    items = [{"tipo": match[0], "numero": int(match[1]), "nombre": match[2].strip(), "tamaño": match[3].strip(), "precio": float(match[4]), "cantidad": int(match[5])} for match in items_matches]
    precio_total = float(patron_precio_total.search(texto_ticket).group(1))
    # Crear un documento para el ticket
    ticket_doc = {
        "numero_pedido": numero_pedido,
        "platos": [item for item in items if item["tipo"] == "Plato" or item["tipo"] =="Bebida"],
        "precio_total": precio_total
    }
   
    return ticket_doc #{'numero_pedido': 3749, 'platos': [{'tipo': 'Plato', 'numero': 1, 'nombre': 'Pizza Margarita de la Casa', 'tamaño': 'Regular', 'precio': 6.44, 'cantidad': 1}], 'precio_total': 6.44}

#Insertar en la base de datos
def insert_bbdd(parseo):
    client = MongoClient("mongodb://localhost:27017/")  
    database = client["menu"]
    tickets_collection = database["tickets"]
    # Insertar el documento en la colección de tickets
    tickets_collection.insert_one(parseo)

    #enviar_notificacion_a_teams(parseo)  #ENVIAR NOTIFICACOIN A TEAMS CON EL NUEVO PLATO 

    # Cerrar la conexión a la base de datos
    client.close()


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



def handle_style_and_responses(user_question: str) -> None:

    """
   Interfaz conversacional con streamlit 

    Args:
        user_question (str): User question
    """
    # Después de recibir la respuesta del chatbot
   

    response = st.session_state.conversation({"question": user_question})
    st.session_state.chat_history = response["chat_history"]

   


    #IMPRIMIR TICKET EN LA CONSOLA AL FINAL E INSERTAR INFO A LA BBDD
    if st.session_state.chat_history is not None:
        # Obtener el último mensaje de la conversación
        last_message = st.session_state.chat_history[-1]
        if "Número de pedido" in last_message.content:
            texto_ticket=last_message.content
            print("Último mensaje:", texto_ticket)
            parseo=parse(texto_ticket)
            insert_bbdd(parseo)
            sys.exit()
            
        

    # Actualiza y almacena la memoria en el estado de la sesión
    st.session_state.conversation_memory = st.session_state.conversation.memory

    human_style = "background-color: #e6f7ff; border-radius: 10px; padding: 10px;"
    chatbot_style = "background-color: #f9f9f9; border-radius: 10px; padding: 10px;"

    

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.markdown(
                f"<p style='text-align: right;'><b>User</b></p> <p style='text-align: right;{human_style}'> <i>{message.content}</i> </p>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"<p style='text-align: left;'><b>Chatbot</b></p> <p style='text-align: left;{chatbot_style}'> <i>{message.content}</i> </p>",
                unsafe_allow_html=True,
            )
    




