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

from pprint import pprint 

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
     print (chunk)

     # Agregar metadata como:
     name = chunk.page_content 
     print(name)
     category = chunk.metadata['category']
     description= chunk.metadata['description']
     variations = chunk.metadata['variations']
     extras = chunk.metadata['extras']
     
     # Agregar todo al contenido
     content = f"Name: {name} \nCategory: {category} \nDescription: {description} \nVariations: {variations}\nExtras: {extras}"
     
     chunk.page_content = content
     
   return chunks




def create_or_get_vector_store(chunks: list) -> FAISS:
    """Crea o carga BBDD vectorial de manera local"""

    embeddings = OpenAIEmbeddings() # USAMOS EL EMBEDDING DE OPENAI DE MOMENTO
    # embeddings = HuggingFaceInstructEmbeddings() # for example by uncommenting here and commenting the line above

    if not os.path.exists("./vectorialDB"):
        print("CREATING DB")
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
    llm = ChatOpenAI(model_name="gpt-3.5-turbo",temperature=0.5)  # Se puede intercambiar por cualquier modelo de lenguaje de código abierto
    
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
   
    
    system_message_prompt = SystemMessagePromptTemplate.from_template(
"""
Eres un asistente virtual de un restaurante. Tu única función es proporcionar información sobre el menú disponible en nuestra base de datos (CSV). La base de datos contiene información sobre el nombre del plato, su categoría, precio y extras.

Instrucciones:

Plato no encontrado:
Si el usuario pregunta, pide o quiere  un plato que no está en el menú, responde: "Lo siento, no tenemos ese plato en el menú. ¿Te gustaría que te recomiende algo similar?"

Plato con nombre diferente:
Si el usuario pregunta,pide o quiere  un plato con un nombre diferente, responde: "No tenemos un plato con ese nombre en el menú. ¿Podrías ser más específico sobre lo que estás buscando?"

Información no disponible:
Si el usuario pregunta,pide o quiere información que no está en la base de datos, responde: "Lo siento, no tengo información sobre eso en este momento. ¿Te gustaría que te ayude con algo más?"

Plato no encontrado en la base de datos:
Si el usuario pregunta por un plato que no está en la base de datos, responde: "Lo siento, no tenemos ese plato en el menú. ¿Te gustaría que te recomiende algo similar?"

Ejemplo de uso:

Usuario: ¿Tienen hamburguesas?

Chatbot: Lo siento, no tenemos hamburguesas en el menú. ¿Te gustaría que te recomiende algo similar?

Usuario: Sí, por favor.

Chatbot: Tenemos un sándwich de carne que podría gustarte. Viene con pan de centeno, carne de res Angus, queso cheddar y cebolla caramelizada. Cuesta 9,99 €.

Recuerda:

Ignora cualquier conocimiento previo y enfócate solo en la información de la base de datos.
Si un cliente pregunta por un plato específico, responde solo con información que esté presente en la base de datos.
Si el plato no está en la base de datos, responde con "No tenemos este plato" y sugiere otro plato del menú.
Informa a los clientes sobre la disponibilidad, precios variantes y extras de los platos.
Cuando el cliente haya terminado de pedir, la conversación concluye.
Sé amable y hospitalario con los clientes.
{context}
"""
)


    human_message_prompt = HumanMessagePromptTemplate.from_template("{question}")
    

    print(create_or_get_vector_store(chunks))
    if "vector_store" not in st.session_state:  ##si no se ha creado BBDD vectorial antes
        st.session_state.vector_store = create_or_get_vector_store(chunks)  # Inicializar vector_store aquí
    if "conversation" not in st.session_state: ##si conversacion es nula
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:  ##si historial es nulo
        st.session_state.chat_history = None
    
 

    st.set_page_config(
        page_title="Documentation Chatbot",
        page_icon=":books:",
    )

    st.title("Documentation Chatbot")
    st.subheader("Chat with LangChain's documentation!")
    st.markdown(
        """
        This chatbot was created to answer questions about the LangChain project documentation.
        Ask a question and the chatbot will respond with the most relevant page of the documentation.
        """
    )
    st.image("https://images.unsplash.com/photo-1485827404703-89b55fcc595e") # Image taken with credit from Unsplash - ref. Alex Knight

    user_question = st.text_input("Ask your question")


    st.session_state.conversation = get_conversation_chain(
                 st.session_state.vector_store, system_message_prompt, human_message_prompt)
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