from flask import Flask, jsonify, request, send_file

import flask
from pymongo import MongoClient
from config import Config 
from flask_cors import CORS
from bson import ObjectId
import os
from bson import Binary
from bson import json_util
import gridfs
from io import BytesIO
import bson 





import base64

import requests

import subprocess


from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity



app = Flask(__name__)
CORS(app)  # Habilitar CORS para toda la aplicación (usar flask en varios puertos del localhost)




app.config.from_object(Config) #carpeta Config contiene  Clave secreta para firmar el token JWT
jwt = JWTManager(app)

client = MongoClient("mongodb://localhost:27017/")



##-----------------------------------------------------------------------------------------------------------------------------------##
##     1.         TABLA USUARIOS 
database = client["menu"]  
usuarios_collection = database["usuarios"] 


##1.1. Crear nuevo usuario 


@app.route("/signup", methods=["POST"])
def signup():
    data = request.json  # Se espera que los datos se envíen como JSON en el cuerpo de la solicitud
    username = data.get("username")
    fullname = data.get("fullname")
    lastname = data.get("lastname")
    phone = data.get("phone")
    email = data.get("email")
    password = data.get("password")
    
    # Verificar si el correo electrónico ya está registrado
    if usuarios_collection.find_one({"email": email}):
        return jsonify({"message": "El correo electrónico ya está registrado"}), 400
    # Verificar si el nombre de usuario ya está en uso
    if usuarios_collection.find_one({"username": username}):
        return jsonify({"message": "El nombre de usuario ya está en uso"}), 400

    # Insertar el nuevo usuario en la colección de usuarios
    usuarios_collection.insert_one({
        "username": username,
        "fullname": fullname,
        "lastname": lastname,
        "phone": phone,
        "email": email,
        "password": password
    })

    return jsonify({"message": "Usuario registrado exitosamente"}), 200



##1.2. Iniciar sesión


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    user = usuarios_collection.find_one({"username": username, "password": password})
    if user:
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token,username=username), 200
    else:
        return jsonify({"message": "Credenciales incorrectas"}), 401


##1.3. Obtenr una tabla con todos los usuarios 
    
@app.route("/users", methods=["GET"])
def get_users():
    users = usuarios_collection.find()
    result = []
    for user in users:
        user["_id"] = str(user["_id"])  # Convertir el objeto id de Mongo en una cadena
        result.append(user)
    return jsonify(result)

##1.4. Borrar un usuario específico 


@app.route("/user/<userid>", methods=["DELETE"])
def delete_user(userid): 
    response = usuarios_collection.delete_one({"_id": ObjectId(userid)})
    
    if response.deleted_count:
        return jsonify({"message": "Usuario borrado correctamente"}), 200

    return jsonify({"message": "Usuario no encontrado"}), 404




###--------------------------------------------------------------------------------------------------------------------
##     2.          INFORMACIÓN SOBRE EL MENÚ 


client_db = client["menu"]
platos_collection = database["platos"]


##2.1. Obtener una tabla con todos los platos del menú 


@app.route("/platos", methods=["GET"])
def get_all_platos():
    platos = platos_collection.find()
    result = []
    for plato in platos:
        plato["_id"] = str(plato["_id"])  # Convertimos el objectid a string
        result.append(plato)
    return jsonify(result)


##refresh_csv.py --> Para poner el menu del dataset en el csv actualizado
def refresh_csv():
    script_path = os.path.join(os.path.dirname(__file__), "../../backend/src/chatbot/get_menu_dataset.py")
    subprocess.call(["python", script_path])


##2.2. Eliminar un plato específico
@app.route("/platos/<plato_id>", methods=["DELETE"])
def delete_plato(plato_id): 
    response = platos_collection.delete_one({"_id": ObjectId(plato_id)})
    
    if response.deleted_count:
        refresh_csv()

        return jsonify({"message": "Plato borrado correctamente"}), 200

    return jsonify({"message": "Plato no encontrado"}), 404

##2.3. Añadir un nuevo un plato 
@app.route("/platos", methods=["POST"])
def add_plato():
    data = request.json
    nombre = data.get("nombre")
    descripcion = data.get("descripcion")
    categoria = data.get("categoria")
    variaciones = data.get("variaciones")

    # Verificar si el nombre del plato ya está en uso
    if platos_collection.find_one({"nombre": nombre}):
        return jsonify({"message": "El nombre del plato ya está en uso"}), 400

    if not nombre or not categoria or not variaciones:
        return jsonify({"message": "Los campos nombre, categoría y variaciones tienen que estar rellenos"}), 400

    # Verificar si todos los precios de las variaciones son positivos
    for variacion in variaciones:
        if 'precio' in variacion and float(variacion['precio']) <= 0:
            return jsonify({"message": "Inserta un precio mayor que cero"}), 400

    new_plato = {
        "nombre": nombre,
        "descripcion": descripcion,
        "categoria": categoria,
        "variaciones": variaciones
    }

    platos_collection.insert_one(new_plato)
    
    refresh_csv()



    return jsonify({"message": "Plato añadido correctamente"}), 201


##2.3. Modificar un plato 
@app.route("/platos/<plato_id>", methods=["PUT"])
def edit_plato(plato_id):
    data = request.json
    nombre = data.get("nombre")
    descripcion = data.get("descripcion")
    categoria = data.get("categoria")
    variaciones = data.get("variaciones")

    if not nombre or not categoria or not variaciones:
        return jsonify({"message": "Los campos nombre, categoría y variaciones tienen que estar rellenos"}), 400

    # Verificar si todos los precios de las variaciones son positivos
    for variacion in variaciones:
        if 'precio' in variacion and float(variacion['precio']) <= 0:
            return jsonify({"message": "Inserta un precio mayor que cero"}), 400

    updated_plato = {
        "nombre": nombre,
        "descripcion": descripcion,
        "categoria": categoria,
        "variaciones": variaciones
    }

    response = platos_collection.update_one({"_id": ObjectId(plato_id)}, {"$set": updated_plato})
    
    if response.modified_count:
        refresh_csv()
        return jsonify({"message": "Plato actualizado correctamente"}), 200

    return jsonify({"message": "Plato no encontrado"}), 404





###--------------------------------------------------------------------------------------------------------------------
##     3.          PERSONALIZACIÓN DE COMPONENTES DE LA APP MÓVIL DESDE LA WEB 

client_db = client["menu"]
personalizacion_collection = client_db["personalización"]  # Crear una colección para la personalización


#EN CASO DE PUT O POST


def save_files(imagen=None): 
        if imagen: 
            fs = gridfs.GridFS(client_db)
            imagen_id=fs.put(imagen)
            return str(imagen_id)
        return None





#EN CASO DE GET
def get_file(file_id):   
    fs = gridfs.GridFS(client_db)
    try:
        return fs.get(ObjectId(file_id)).read()
    except Exception as err:
        print(f'Error getting file: {err}')

@app.route("/app_customization"+ '/file/<file_id>', methods=['GET'])  #Muestra cotenido de la imagen si pongo id de esa imagen de la bbdd
def serve_pdf(file_id):
    photo = get_file(file_id)
    return send_file(BytesIO(photo), mimetype='application/png', as_attachment=False,)

##3.1. Obtener la información de personalización de la app móvil
@app.route("/app_customization", methods=["GET"])
def get_personalizacion():
    personalizacion = personalizacion_collection.find_one({})
    if personalizacion:
        return jsonify(json_util.dumps(personalizacion)), 200
    else:
        return jsonify({"message": "Información de personalización no encontrada"}), 404


##3.2. Actualizar la información de personalización de la app móvil

@app.route("/app_customization", methods=["PUT"])

def update_personalizacion():
    nombre_restaurante = request.form.get("nombre_restaurante")
    logo_principal_file = request.files['logo_principal'] if 'logo_principal' in request.files else None
    logo_secundario_file = request.files['logo_secundario'] if 'logo_secundario' in request.files else None

    print(f"nombr_restaurante: {nombre_restaurante}")
    print(f"logo_principal_file: {logo_principal_file}")
    print(f"logo_secundario_file: {logo_secundario_file}")

    fields_to_set = {}

    if nombre_restaurante:
        fields_to_set["nombre_restaurante"] = nombre_restaurante

    if logo_principal_file:
        logo_principal = save_files(logo_principal_file)
        fields_to_set["logo_principal"] = logo_principal

    if logo_secundario_file:
        logo_secundario = save_files(logo_secundario_file)
        fields_to_set["logo_secundario"] = logo_secundario

    print(f"fields_to_set: {fields_to_set}")

    if fields_to_set:
        result = personalizacion_collection.update_one({}, {"$set": fields_to_set}, upsert=True)
        print(f"Update result: {result}")

    return jsonify({"message": "Información de personalización actualizada correctamente"}), 200



##3.3. Añadir una nueva personalizacion (POST) (Aunque no lo usaremos, nos servirá unicamente para probar que todo funciona bien)
@app.route("/app_customization", methods=["POST"])
def create_personalizacion():
    nombre_restaurante = request.form.get("nombre_restaurante")
    logo_principal_file = request.files.get("logo_principal")
    logo_secundario_file = request.files.get("logo_secundario")

    if not logo_principal_file or not logo_secundario_file or not nombre_restaurante:
        return jsonify({"message": "Los campos nombre_restaurante, logo_principal y logo_secundario son obligatorios"}), 400

    try:
        logo_principal_funcionOuael = save_files(imagen=logo_principal_file)
        logo_secundario_funcionOuael = save_files(imagen=logo_secundario_file)
    except Exception as e:
        return jsonify({"message": "Error al leer los archivos adjuntos: {}".format(str(e))}), 500

    personalizacion_collection.insert_one({
        "nombre_restaurante": nombre_restaurante,
        "logo_principal": logo_principal_funcionOuael,
        "logo_secundario": logo_secundario_funcionOuael
    })

    return jsonify({"message": "Información de personalización creada correctamente"}), 201



@app.route("/app_customization/primer_oid", methods=["GET"])
def obtener_primer_oid():
    documento = personalizacion_collection.find_one()
    if documento:
        nombre_restaurante = documento.get("nombre_restaurante")
        logo_principal_oid = str(documento.get("logo_principal", None))
        logo_secundario_oid = str(documento.get("logo_secundario", None))
        
        return jsonify({
            "nombre_restaurante": nombre_restaurante,
            "logo_principal_oid": logo_principal_oid,
            "logo_secundario_oid": logo_secundario_oid
        }), 200
    else:
        return jsonify({"mensaje": "No se encontró ningún documento"}), 404

if __name__ == "__main__":
    app.run(debug=True)

if __name__ == "__main__":
    app.run(debug=True)

