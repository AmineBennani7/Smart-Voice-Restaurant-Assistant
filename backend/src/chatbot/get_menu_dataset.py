import pandas as pd
import os
from pymongo import MongoClient
from tqdm import tqdm
from trafilatura.sitemaps import sitemap_search
from trafilatura import fetch_url, extract, extract_metadata


# Conectarse a MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["menu"] ##bdbd menu
collection = db["platos"] ##tabla principal=Platos



def create_dataset():


  data = []

  cursor = collection.find()  ##realiza una consulta en todos los elementos de la tablaplatos
                                ## servira para hacer tqdm (cursor de barra de progreso )
 
 
  for doc in tqdm(cursor, total=collection.count_documents({})):  ##tqdm, cursor de barra de progreso

    ##Añado cada una de las columnas de la bbdd para luego añadirlo a la lista data
    name = doc["nombre"]
    category = doc["categoria"]
    description= doc["descripcion"]
    variations = doc["variaciones"]
   

    d = {
      "name": name,
      "category": category,  
      "description" : description,
      "variations": variations,   
      
    }

    data.append(d)
   #Finalmente lo añado al dataframe
  df = pd.DataFrame(data)

  # Eliminar filas con datos faltantes  (REPASAR, PUEDE QUE Hayan PLATOS que no tengan extras)
  df.dropna(inplace=True)

  current_dir = os.path.dirname(os.path.abspath(__file__))
  data_dir = os.path.join(current_dir, "..", "chatbot")
  output_file = os.path.join(data_dir, "menu_dataset", "menus_dataset.csv")


   

  # Guardar DataFrame como CSV
  df.to_csv(output_file, index=False)

  return df

if __name__ == "__main__":

  df = create_dataset()