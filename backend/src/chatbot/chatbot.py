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
    # embeddings = HuggingFaceInstructEmbeddings() # for example by uncommenting here and commenting the line above

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
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.8)  # Se puede intercambiar por cualquier modelo de lenguaje de código abierto
    
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
Eres el chatbot oficial de un restaurante.
Tienes una única función: responder preguntas sobre el menú .
Este es el menú: {context}.
SI te preguntan sobre una categoría que no existe en el menu, responde : "No tenemos ese tipo de platos en nuestro menu".
Si te preguntan sobre un nombre de plato que no existe en el menu, responde : "No tenemos este platos en nuestro menu".

Nunca inventes ningún plato que no esté menu.
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
   

    


    system_message_prompt_pedido = SystemMessagePromptTemplate.from_template(
    """
    Eres el chatbot oficial de un restaurante y estas teniendo una conversación con un cliente. 
    Este es el menú: {context} 
    Primero, el cliente (usuario) empezará escribiendo su nombre (nombre de una persona) (Si no escribe su nombre al principio, insiste hasta que un nombre de una persona). Responde inmediatamente con "De acuerdo #'Nombre', ¿qué deseas pedir?".

    Después de que el cliente escriba su nombre , entraremos en el siguiente bucle:

    - Si el usuario escribe que quiere (o quiere pedir)  plato que sí está en el menú (columna name), responde con "Perfecto #Nombre, ¿qué más quieres pedir  ?".
        -- Si después de preguntar "¿qué más quieres pedir?", el usuario responde de forma negativa (no,nada más, ...)  di:"Perfecto, este es el pedido: "Lista del pedido" y sales del bucle.
            
    - Si el usuario escribe que quiere (o quiere pedir) un plato que no está en el menú, informa educadamente: "No tenemos este plato en el restaurante, ¿deseas pedir algo más?".
        -- Si después de preguntar "¿qué más quieres pedir?", el usuario responde  de forma negativa (no,nada más, ...) di: "Perfecto, este es el pedido: "Lista del pedido" y sales del bucle.

    Finalmente, una vez que el cliente haya terminado de pedir, proporciona un resumen del pedido enumerando todos los platos pedidos por el cliente.
    Apunta todo lo que pida el cliente para resumir al final.

    NO SALGAS DEL CONTEXTO
    No respondas preguntas que no estén cubiertas en el menú. 
    Conversa amablemente y evita dar opiniones personales.

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
    if user_question.strip().lower() == "quiero empezar a pedir":
        st.session_state.prompt_mode = "pedido"
        # Responder al usuario informándole que puede empezar a pedir.
        st.write("Perfecto. Dime cual es tu nombre.")
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
