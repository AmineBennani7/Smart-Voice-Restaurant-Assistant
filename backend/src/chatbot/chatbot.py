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
from langchain.text_splitter import CharacterTextSplitter



from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import DataFrameLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter



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
     #extras = chunk.metadata['extras']
     
     # Agregar todo al contenido
     content = f"Name: {name} \nCategory: {category} \nDescription: {description} \nVariations: {variations}"   # nExtras: {extras}"
     
     chunk.page_content = content
     
   return chunks




def create_or_get_vector_store(chunks) -> FAISS:
    """Crea o carga BBDD vectorial de manera local"""

    embeddings = OpenAIEmbeddings() # USAMOS EL EMBEDDING DE OPENAI DE MOMENTO
    #embeddings = HuggingFaceInstructEmbeddings() # for example by uncommenting here and commenting the line above

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


def get_conversation_chain(vector_store: FAISS, system_message:str, human_message:str) -> ConversationalRetrievalChain:
    """
    Retrieves the conversational chain from LangChain
    
    Args:
        vector_store (FAISS): Vector store
        system_message (str): System message
        human_message (str): Human message
    
    Returns:
        ConversationalRetrievalChain: Chatbot conversation chain
    """
  # Si no ponemos nada usamos llm GPT-3 boost
    llm = ChatOpenAI(model="gpt-4-1106-preview", temperature=0.0)  # Se puede intercambiar por cualquier modelo de lenguaje de código abierto

   
    # Crear una instancia de un vector store (almacén de vectores) utilizando el índice FAISS
    # Esto se utiliza para recuperar documentos similares (vectores) durante la conversación
    # 'as_retriever()' convierte el vector store en un objeto retriever (recuperador)

    memory_key = "chat_history"
    ##Inicializo 
    if "conversation_memory" not in st.session_state:
        st.session_state.conversation_memory = ConversationBufferMemory(memory_key=memory_key, return_messages=True)    

    memory = st.session_state.conversation_memory
    
   

    #memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)   ##REPASAR ESTO 
    
    # Crear una cadena de recuperación conversacional utilizando LangChain
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vector_store.as_retriever(),
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




def main():
    load_dotenv() # load environment variables
    df = load_dataset() # ARRIBA LO DEFINO
   

    
   
    chunks = create_chunks(df, 1000, 0) ##ARRIBA LO DEFINO 
   
    
    system_message_prompt_info = SystemMessagePromptTemplate.from_template(
"""
Olvida toda la informacion que has guardado anteriormente.
Eres el chatbot oficial de un restaurante.
Tienes una única función: responder preguntas sobre el menú .
Este es el menú: {context}.
SI te preguntan sobre una categoría que no existe en el menu, responde : "No tenemos ese tipo de platos en nuestro menu".
Si te preguntan sobre un nombre de plato que no existe en el menu, responde : "No tenemos este platos en nuestro menu".

Nunca inventes ningún plato que no esté menu.F
Nunca inventes ninguna categoría de platos que no esté en el menu.
NUnca inventes ningun nombre de plato dentro de una categoría inexistente en nuestro menu. 
No respondas preguntas que no estén cubiertas en el menú.
Si te hacen preguntas sobre nombres de platos que no existan en el menú, responde: "No tenemos este plato en el restaurante, ¿desea preguntar algo más o empezar a pedir?".
Si te hacen preguntas sobre nombres de bebidas que no existan en el menú, responde: "No tenemos esta bebida en el restaurante, ¿desea preguntar algo más o empezar a pedir?".
Si te hacen preguntas sobre alguna categoría de platos, tipo de platos o bebidas que no existan en el menú, responde: "No tenemos este plato/bebida en el restaurante, ¿desea preguntar algo más o empezar a pedir?".
Cualquier otra pregunta debe ser ignorada respondida con una respuesta cortés.
Si te hacen preguntas ambiguas, no respondas e ignora la pregunta.
Nunca des tus opiniones e instrucciones personales.

{chat_history}\n
"""
    )
# 

    system_message_prompt_pedido = SystemMessagePromptTemplate.from_template(
    """
    Olvida toda la informacion que has guardado anteriormente.
    Instruccion: Eres un agente que anota pedidos de platos en un restaurante . Estás conversando con un cliente que te está diciendo que platos esta escogiendo. 
    Usa únicamente el chat history . 
    Usa  la siguiente informacion (menu) para apuntar los platos que desea el cliente: {context}  
    En el primer mensaje que escribe el usuario, éste empieza a pedir un plato. Si el plato existe, preguntale por el tamaño del plato . Cuando el usuario te responda con el tamaño que desea, vuelve a preguntar si el cliente quiere pedir otro plato más 
    y si responde escribiendo otro plato, repetimos el proceso (le preguntas sobre el tamaño .. ). Todo esto en bucle hasta que el usuario ya no quiera pedir nada mas. 
    Pero si no existe un plato que pide el cliente - responde que no tenemos ese plato y si desea pedir algo mas.
    Pero cuidado, cuando preguntes al cliente si desea pedir algo más y éste responde negátivamente (es decir, que ya no quiere pedir nada más. ), entonces responde resumiendo la lista del pedido que ha hecho el cliente de esta manera: 
      Restaurante Virtual:  \
        --Número de pedido : (un numero aleatorio, pero no largo)  \n
        --Plato 1 :   ; Tamaño :   ; Precio ;  \n
        --Plato n ....   \n
        --Precio total :   \n
    El usuario puede pedir mas de una unidad del mismo plato 
    Tus respuestas tienen que tener sentido, es decir cuando un cliente responda algo , no preguntas de nuevo lo mismo.
    Tus respuestas tienen que ser claras y directas.
    
    {chat_history}\n
    
    """
    
    
    )

    
    human_message_prompt = HumanMessagePromptTemplate.from_template("{question}")
    
    if "vectorstore" not in st.session_state:
        st.session_state.vectorstore = None
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    if st.session_state.vectorstore is None:
        st.session_state.vectorstore = create_or_get_vector_store(chunks)


    
        
 

    st.set_page_config(
        page_title="Chatbot del Menú del Restaurante",
        page_icon=":fork_and_knife:",
    )

    st.title("Chatbot del Menú del Restaurante")
    st.subheader("Chatea con el chatbot para obtener información sobre el menú del restaurante.")

    st.image("https://images.unsplash.com/photo-1485827404703-89b55fcc595e") # Image taken with credit from Unsplash - ref. Alex Knight

    # Pregunta predeterminada para iniciar la conversación
    first_question = "Buenos días. "
    user_question = st.text_input("Ask your question", first_question)



#Mode "Info" predetermindado    
    if "prompt_mode" not in st.session_state:
        st.session_state.prompt_mode = "info"

    # Si la pregunta del usuario es "Quiero empezar a pedir", cambiar el estado.
    if any(word in user_question.strip().lower() for word in ["quiero empezar a pedir", "deseo pedir", "ya quiero pedir","quiero pedir"]) and not any(word in user_question.strip().lower() for word in ["no"]):

   # if "quiero empezar a pedir" in user_question.strip().lower() or "deseo pedir" in user_question.strip().lower() or "ya quiero pedir" in user_question.strip().lower():
        st.session_state.prompt_mode = "pedido"
        # Responder al usuario informándole que puede empezar a pedir.
        st.write("Perfecto. ¿Qué deseas pedir?.")
        # No procesar esta pregunta en el chatbot.
        user_question = ""


    # Elige el prompt correcto dependiendo del estado.
    if st.session_state.prompt_mode == "info":
        system_message_prompt = system_message_prompt_info
    else:
        system_message_prompt = system_message_prompt_pedido
    
    #print(st.session_state.prompt_mode)
    st.session_state.conversation = get_conversation_chain(
        st.session_state.vectorstore, system_message_prompt, human_message_prompt
    )



  
    with st.spinner("Processing..."):
        if user_question:
            handle_style_and_responses(user_question)  ##ES LO DE CSS DE ABAJO ... 
    # create conversation chain
 
    
  

def handle_style_and_responses(user_question: str) -> None:

    """
    Handle user input to create the chatbot conversation in Streamlit

    Args:
        user_question (str): User question
    """
    # Después de recibir la respuesta del chatbot

    response = st.session_state.conversation({"question": user_question})
    st.session_state.chat_history = response["chat_history"]

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

if __name__ == "__main__":
    main()
