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

    if not os.path.exists("./backend/src/vectorialDB"):
        print("CREATING DB")
        vectorstore = FAISS.from_documents(
            chunks, embeddings
        )
        vectorstore.save_local("./backend/src/vectorialDB")
    else:
        print("LOADING DB")
        vectorstore = FAISS.load_local("./backend/src/vectorialDB", embeddings)

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
    llm = ChatOpenAI(temperature=0.5)  # Se puede intercambiar por cualquier modelo de lenguaje de código abierto
    
    # Crear una instancia de un vector store (almacén de vectores) utilizando el índice FAISS
    # Esto se utiliza para recuperar documentos similares (vectores) durante la conversación
    # 'as_retriever()' convierte el vector store en un objeto retriever (recuperador)

    memory_key = "chat_history"

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
   #print (df)
    chunks = create_chunks(df, 1000, 0) ##ARRIBA LO DEFINO 
    
    system_message_prompt = SystemMessagePromptTemplate.from_template(
        """
        Eres un asistente virtual de un restaurante. Tu papel es hablar con los clientes de un restaurente y responderles a las preguntas o peticiones que tienen 
        sobre el menu que se encuentra en la base de datos. Descarta toda la información anterior que tienes sobre el ámbito de la comida, solo ten en cuenta los platos que existen en nuestra base de datos y su informacion correspondiente.
        Informa a los clientes de la disponibilidad de los platos existentes en el menú, si no encuentras un plato en el menu debes contestar 'No tenemos este plato' y propon otro plato del menu en su lugar.
        informa a los clientes de los precios variantes y extras.
          Una vez terminan de pedir la comida, la conversacion acaba con ello. Tienes que ser muy hospitalario con los clientes .
        Si no existe alguna información solicitada por el cliente en la base de datos sobre algún plato, conesta que 'No tengo información sobre esa pregunta' y propon otro plato existente en el menú\n
        {context}
        """
    )
    human_message_prompt = HumanMessagePromptTemplate.from_template("{question}")
    
    st.session_state.vector_store = create_or_get_vector_store(chunks)

    if "vector_store" not in st.session_state:  ##si no se ha creado BBDD vectorial antes"
        st.session_state.vector_store = create_or_get_vector_store(chunks)
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

    with st.spinner("Processing..."):
        if user_question:
            handle_style_and_responses(user_question)  ##ES LO DE CSS DE ABAJO ... 

     # create conversation chain
            st.session_state.conversation = get_conversation_chain(
                 st.session_state.vector_store, system_message_prompt, human_message_prompt
    )


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