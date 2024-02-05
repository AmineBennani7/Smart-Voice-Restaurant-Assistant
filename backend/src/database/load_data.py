##pip install pymongo
from pymongo import MongoClient

def load_data():
   
    client = MongoClient("mongodb://localhost:27017/")  
    database = client["menu"]  # Reemplaza con el nombre real de tu base de datos
    collection = database["platos"]  # Reemplaza con el nombre deseado para tu colección

    # Agregar datos manualmente
    datos_nuevos = [
  {
    "categoria": "Pasta",
    "nombre": "Spaghetti Bolognese",
    "descripcion": "Spaghetti con salsa bolognesa",
    "variaciones": [
      {
        "variacion": "Tamaño regular",
        "precio": 9.99
      },
      {
        "variacion": "Tamaño grande",
        "precio": 12.99
      }
    ],
    "extras": [
      {
        "extra": "Albóndigas",
        "precio": 2.50
      },
      {
        "extra": "Queso parmesano",
        "precio": 1.50
      }
    ]
  },
  {
    "categoria": "Pasta",
    "nombre": "Fettuccine Alfredo",
    "descripcion": "Fettuccine con salsa Alfredo cremosa",
    "variaciones": [
      {
        "variacion": "Tamaño regular",
        "precio": 10.99
      },
      {
        "variacion": "Tamaño grande",
        "precio": 14.99
      }
    ],
    "extras": [
      {
        "extra": "Pollo a la parrilla",
        "precio": 3.50
      },
      {
        "extra": "Broccoli",
        "precio": 2.00
      }
    ]
  },]
 


    
    collection.insert_many(datos_nuevos)

    # Cerrar la conexión a MongoDB
    client.close()

if __name__ == "__main__":
    load_data()