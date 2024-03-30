##pip install pymongo
from pymongo import MongoClient

def load_data():
   
    client = MongoClient("mongodb://localhost:27017/")  
    database = client["menu"]  
    collection = database["platos"]  
  # Eliminar la colección existente
    collection.drop()
 
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
  }, 
      {
        "categoria": "Calzone",
        "nombre": "Calzone de York y Queso",
        "descripcion": "Tomate, york, mozzarella y ricotta",
        "variaciones": [{"variacion": "Tamaño regular", "precio": 9.04}],
    },
    {
        "categoria": "Calzone",
        "nombre": "Calzone de Atún",
        "descripcion": "Tomate, queso, atún, cebolla, aceitunas y ricotta",
        "variaciones": [{"variacion": "Tamaño regular", "precio": 9.04}],
    },
    
    {
        "categoria": "Pizza clásica",
        "nombre": "Pizza Margarita de la Casa",
        "descripcion": "Contiene gluten y lácteos",
        "variaciones": [
            {"variacion": "Tamaño regular", "precio": 6.44},
            {"variacion": "Tamaño grande", "precio": 7.74},
        ],
    },
    {
        "categoria": "Pizza clásica",
        "nombre": "Pizza York y Queso",
        "descripcion": "Contiene gluten y lácteos",
        "variaciones": [
            {"variacion": "Tamaño regular", "precio": 7.15},
            {"variacion": "Tamaño grande", "precio": 8.45},
        ],
    },
    {
        "categoria": "Pizza clásica",
        "nombre": "Pizza Atún y Bacon",
        "descripcion": "Contiene gluten, lacteos, pescado y soja",
        "variaciones": [
            {"variacion": "Tamaño regular", "precio": 7.15},
            {"variacion": "Tamaño grande", "precio": 8.45},
        ],
    },
    {
        "categoria": "Pizza clásica",
        "nombre": "Pizza Atún y York",
        "descripcion": "Contiene gluten, pescado y lácteos",
        "variaciones": [
            {"variacion": "Tamaño regular", "precio": 7.15},
            {"variacion": "Tamaño grande", "precio": 8.45},
        ],
    },
    {
        "categoria": "Pizza clásica",
        "nombre": "Pizza Cheddar y Bacon",
        "descripcion": "Contiene gluten, lácteos y soja",
        "variaciones": [
            {"variacion": "Tamaño regular", "precio": 7.74},
            {"variacion": "Tamaño grande", "precio": 9.04},
        ],
    },
    {
        "categoria": "Pizza clásica",
        "nombre": "Pizza Doble Pepperoni",
        "descripcion": "Contiene gluten, soja, lácteos y mostaza",
        "variaciones": [
            {"variacion": "Tamaño regular", "precio": 7.74},
            {"variacion": "Tamaño grande", "precio": 9.04},
        ],
    },
    {
        "categoria": "Pizza clásica",
        "nombre": "Pizza Cuatro Estaciones",
        "descripcion": "Cebolla, pimiento, champiñones y jamón york",
        "variaciones": [
            {"variacion": "Tamaño regular", "precio": 7.74},
            {"variacion": "Tamaño grande", "precio": 9.04},
        ],
    },
    {
        "categoria": "Pizza clásica",
        "nombre": "Pizza Carbonara Francesa",
        "descripcion": "Crema carbonara francesa con nata, bacon, cebolla y champiñon",
        "variaciones": [
            {"variacion": "Tamaño regular", "precio": 7.74},
            {"variacion": "Tamaño grande", "precio": 9.04},
        ],
    },
    {
        "categoria": "Pizza clásica",
        "nombre": "Pizza Cuatro Queso",
        "descripcion": "Con mozzarella, cheddar, queso azul y queso de cabra",
        "variaciones": [
            {"variacion": "Tamaño regular", "precio": 8.45},
            {"variacion": "Tamaño grande", "precio": 9.75},
        ],
    },
    {
        "categoria": "Pizza clásica",
        "nombre": "Pizza Serrana",
        "descripcion": "Tomate natural, cebolla, bacon, ajo asado, aove y jamón serrano",
        "variaciones": [
            {"variacion": "Tamaño regular", "precio": 8.45},
            {"variacion": "Tamaño grande", "precio": 9.75},
        ],
    },
     {
            "categoria": "Pizza especial",
            "nombre": "Pizza Budare",
            "descripcion": "Con borde de queso, pepperoni, maíz, york y aceitunas negras.",
            "variaciones": [
                {"variacion": "Tamaño regular", "precio": 12.35},
                {"variacion": "Tamaño grande", "precio": 13.70},  
            ],
        },
        {
            "categoria": "Pizza especial",
            "nombre": "Pizza Amor de Madre",
            "descripcion": "Pepperoni, bacon y cebolla",
            "variaciones": [{"variacion": "Tamaño regular", "precio": 8.45}],
        },
        {
            "categoria": "Pizza especial",
            "nombre": "Pizza Roma Mía",
            "descripcion": "Queso mozzarella, pepperoni, bacon y maíz",
            "variaciones": [{"variacion": "Tamaño regular", "precio": 8.45}],
        },
        {
            "categoria": "Pizza especial",
            "nombre": "Pizza Vilvaldi",
            "descripcion": "Cebolla, pimiento, aceitunas, champiñones, bacon y salsa césar",
            "variaciones": [{"variacion": "Tamaño regular", "precio": 8.45}],
        },
        {
            "categoria": "Pizza especial",
            "nombre": "Pizza Carnival",
            "descripcion": "Cerdo desmechado, pollo asado, bacon, cebolla y salsa gaucha",
            "variaciones": [
                {"variacion": "Tamaño regular", "precio": 9.04},
                {"variacion": "Tamaño grande", "precio": 10.39},  
            ],
        },
        {
            "categoria": "Pizza especial",
            "nombre": "Pizza La Regenta",
            "descripcion": "Queso de cabra, pimiento y nueces",
            "variaciones": [
                {"variacion": "Tamaño regular", "precio": 9.04},
                {"variacion": "Tamaño grande", "precio": 10.39},  
            ],
        },
        {
            "categoria": "Pizza especial",
            "nombre": "Pizza Hawai",
            "descripcion": "La pizza más polémica - Piña, york y bacon...",
            "variaciones": [
                {"variacion": "Tamaño regular", "precio": 9.04},
                {"variacion": "Tamaño grande", "precio": 10.39},  
            ],
        },
        {
            "categoria": "Pizza especial",
            "nombre": "Pizza Normanda",
            "descripcion": "Roqueford, anchoas y alcaparras",
            "variaciones": [
                {"variacion": "Tamaño regular", "precio": 9.75},
                {"variacion": "Tamaño grande", "precio": 11.10},  
            ],
        },
        {
            "categoria": "Pizza especial",
            "nombre": "Pizza Primavera",
            "descripcion": "Tomate en rodajas, cebolla, pavo, albahaca y AOVE",
            "variaciones": [
                {"variacion": "Tamaño regular", "precio": 9.04},
                {"variacion": "Tamaño grande", "precio": 10.39},  
            ],
        },
        {
            "categoria": "Pizza especial",
            "nombre": "Pizza El Mariachi",
            "descripcion": "Para los amantes del picante - Pimiento, cebolla, jalapeños, pollo cajún y salsa picante",
            "variaciones": [
                {"variacion": "Tamaño regular", "precio": 9.75},
                {"variacion": "Tamaño grande", "precio": 11.10},  
            ],
        },
        {
            "categoria": "Pizza vegetariana",
            "nombre": "Pizza La Clásica",
            "descripcion": "Cebolla, pimiento, tomate, ajo, champiñones y AOVE",
            "variaciones": [
                {"variacion": "Tamaño regular", "precio": 9.04},
                {"variacion": "Tamaño grande", "precio": 10.39},  
            ],
        },
        {
            "categoria": "Pizza vegetariana",
            "nombre": "Pizza Griega",
            "descripcion": "Tomate en rodajas, aceitunas negras, cebolla, queso fresco y salsa césar",
            "variaciones": [
                {"variacion": "Tamaño regular", "precio": 9.04},
                {"variacion": "Tamaño grande", "precio": 10.39},  
            ],
        },
        {
            "categoria": "Pizza vegetariana",
            "nombre": "Pizza Asturiana",
            "descripcion": "Queso de cabra, tomate natural, orégano y romero",
            "variaciones": [
                {"variacion": "Tamaño regular", "precio": 9.04},
                {"variacion": "Tamaño grande", "precio": 10.39},  
            ],
        },
        {
            "categoria": "Pizza vegetariana",
            "nombre": "Pizza Bianca Chesa",
            "descripcion": "Queso brie, miel y nueces",
            "variaciones": [
                {"variacion": "Tamaño regular", "precio": 9.75},
                {"variacion": "Tamaño grande", "precio": 11.10},  
            ],
        },
         {
            "categoria": "Bebidas",
            "nombre": "Botella de Agua, pequeña",
            "descripcion": "",
            "variaciones": [
                {"variacion": "Único", "precio": 1.30},
            ],
        },
        {
            "categoria": "Bebidas",
            "nombre": "Botella de Agua Grande",
            "descripcion": "",
            "variaciones": [
                {"variacion": "Único", "precio": 1.80},
            ],
        },
        {
            "categoria": "Bebidas",
            "nombre": "Coca Cola, Lata",
            "descripcion": "",
            "variaciones": [
                {"variacion": "Único", "precio": 2.30},
            ],
        },
        {
            "categoria": "Bebidas",
            "nombre": "Coca Cola Zero, Lata",
            "descripcion": "",
            "variaciones": [
                {"variacion": "Único", "precio": 2.30},
            ],
        },
        {
            "categoria": "Bebidas",
            "nombre": "Fanta Naranja, Lata",
            "descripcion": "",
            "variaciones": [
                {"variacion": "Único", "precio": 2.20},
            ],
        },
        {
            "categoria": "Bebidas",
            "nombre": "Fanta Limón, Lata",
            "descripcion": "",
            "variaciones": [
                {"variacion": "Único", "precio": 2.20},
            ],
        },
        {
            "categoria": "Bebidas",
            "nombre": "Nestea, Lata",
            "descripcion": "",
            "variaciones": [
                {"variacion": "Único", "precio": 2.40},
            ],
        },
        {
            "categoria": "Bebidas",
            "nombre": "Nestea Maracuya, Lata",
            "descripcion": "",
            "variaciones": [
                {"variacion": "Único", "precio": 2.40},
            ],
        },
        {
            "categoria": "Bebidas",
            "nombre": "Aquarius Naranja, Lata",
            "descripcion": "",
            "variaciones": [
                {"variacion": "Único", "precio": 2.20},
            ],
        },
        {
            "categoria": "Bebidas",
            "nombre": "Aquarius Limón, Lata",
            "descripcion": "",
            "variaciones": [
                {"variacion": "Único", "precio": 2.20},
            ],
        },
        {
            "categoria": "Bebidas",
            "nombre": "Estrella Sur, Botellín",
            "descripcion": "",
            "variaciones": [
                {"variacion": "Único", "precio": 1.30},
            ],
        },
        {
            "categoria": "Bebidas",
            "nombre": "Alhambra,",
            "descripcion": "",
            "variaciones": [
                {"variacion": "Único", "precio": 2.50},
            ],
        },
        {
            "categoria": "Bebidas",
            "nombre": "Coca cola 2L ",
            "descripcion": "",
            "variaciones": [
                {"variacion": "Único", "precio": 2.60},
            ],
        },
        {
            "categoria": "Bebidas",
            "nombre": "Cruz Campo de 1 L",
            "descripcion": "",
            "variaciones": [
                {"variacion": "Único", "precio": 2.50},
            ],
        },
        {
            "categoria": "Bebidas",
            "nombre": "Maltin polar",
            "descripcion": "Bebida de malta. 207 ml",
            "variaciones": [
                {"variacion": "Único", "precio": 1.90},
            ],
        },
    ]

  
  
  
  
 


    
    collection.insert_many(datos_nuevos)

    # Cerrar la conexión a MongoDB
    client.close()

if __name__ == "__main__":
    load_data()