from flask import Flask, jsonify, request, send_file

import flask
from pymongo import MongoClient
from config import Config 
from flask_cors import CORS
from bson import ObjectId
import os
from bson import json_util
import gridfs
from io import BytesIO
from werkzeug.security import generate_password_hash, check_password_hash


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
    password_hash = generate_password_hash(password)  # Guardar el hash de la contraseña, no la contraseña en sí

    
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
        "password": password_hash
    })

    return jsonify({"message": "Usuario registrado exitosamente"}), 200



##1.2. Iniciar sesión


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    user = usuarios_collection.find_one({"username": username})
    if user and check_password_hash(user['password'], password):  # Verificar la contraseña contra el hash almacenado
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token,username=username), 200
    else:
        return jsonify({"message": "Credenciales incorrectas"}), 401


##1.3. Obtener una tabla con todos los usuarios 
    
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

#1.5.Modificar contraseña:
# Ruta para modificar la contraseña de un usuario específico
@app.route("/change_password/<username>", methods=["PUT"])
@jwt_required()
def change_password(username):
    current_user = get_jwt_identity()  # Obtener el usuario actual desde el token JWT
    data = request.json  # Obtener los datos enviados en la solicitud
    current_password = data.get("current_password")
    new_password = data.get("new_password")

    if not current_password or not new_password:
        return jsonify({"message": "Se requieren ambos campos: contraseña actual y nueva contraseña"}), 400

    user = usuarios_collection.find_one({"username": username})
    if not user:
        return jsonify({"message": "El usuario especificado no existe"}), 404

    if current_user != username:
        return jsonify({"message": "No tienes permiso para cambiar la contraseña de otro usuario"}), 403

    if not check_password_hash(user['password'], current_password):
        return jsonify({"message": "La contraseña actual es incorrecta"}), 401

    new_password_hash = generate_password_hash(new_password)
    usuarios_collection.update_one({"username": username}, {"$set": {"password": new_password_hash}})
    return jsonify({"message": "Contraseña actualizada correctamente"}), 200



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



#get categorias para las piecharts
@app.route("/categorias", methods=["GET"])
def get_categorias():
    categorias = platos_collection.distinct("categoria")
    return jsonify(categorias)



###--------------------------------------------------------------------------------------------------------------------
##     3.          PERSONALIZACIÓN DE COMPONENTES DE LA APP MÓVIL DESDE LA WEB 

client_db = client["menu"]
personalizacion_collection = client_db["personalización"]  # 

def save_files(imagen=None):  #Dado una imagen, retorna su id para guardarla en la bd 
        if imagen: 
            fs = gridfs.GridFS(client_db)
            imagen_id=fs.put(imagen)
            return str(imagen_id)
        return None


def get_file(file_id):   #Dada una id de un fichero (imagen) en la bd, la devuelve a imagen 
    fs = gridfs.GridFS(client_db)
    try:
        return fs.get(ObjectId(file_id)).read()
    except Exception as err:
        print(f'Error getting file: {err}')
        


##3.1. Obtener la información de personalización de la app móvil
@app.route("/app_customization", methods=["GET"])
def get_personalizacion():
    personalizacion = personalizacion_collection.find_one({})
    if personalizacion:
        return jsonify(json_util.dumps(personalizacion)), 200
    else:
        return jsonify({"message": "Información de personalización no encontrada"}), 404
    

#3.2. A partir de la id de una imagen , devuelve en formato PNG 
@app.route("/app_customization"+ '/file/<file_id>', methods=['GET'])  
def serve_picture(file_id):
    photo = get_file(file_id)
    return send_file(BytesIO(photo), mimetype='application/png', as_attachment=False,)


##3.3. Actualizar la información de personalización de la app móvil
@app.route("/app_customization", methods=["PUT"])

def update_personalizacion():
    nombre_restaurante = request.form.get("nombre_restaurante") #Request: Saca el contenido del formulario 
    logo_principal_file = request.files['logo_principal'] if 'logo_principal' in request.files else None
    logo_secundario_file = request.files['logo_secundario'] if 'logo_secundario' in request.files else None

   
    #Si hay un campo vacio en el form, no lo modificamos
    fields_to_set = {}

    if nombre_restaurante:
        fields_to_set["nombre_restaurante"] = nombre_restaurante

    if logo_principal_file:
        logo_principal = save_files(logo_principal_file)
        fields_to_set["logo_principal"] = logo_principal

    if logo_secundario_file:
        logo_secundario = save_files(logo_secundario_file)
        fields_to_set["logo_secundario"] = logo_secundario

    if fields_to_set:
        result = personalizacion_collection.update_one({}, {"$set": fields_to_set}, upsert=True)
        print(f"Update result: {result}")

    return jsonify({"message": "Información de personalización actualizada correctamente"}), 200



##3.4. Añadir una nueva personalizacion (POST) (Aunque no lo usaremos, nos servirá unicamente para probar que todo funciona bien)
@app.route("/app_customization", methods=["POST"])
def create_personalizacion():
    nombre_restaurante = request.form.get("nombre_restaurante") #Saco los elementos del form 
    logo_principal_file = request.files.get("logo_principal")
    logo_secundario_file = request.files.get("logo_secundario")

    if not logo_principal_file or not logo_secundario_file or not nombre_restaurante:
        return jsonify({"message": "Los campos nombre_restaurante, logo_principal y logo_secundario son obligatorios"}), 400

    try:
        logo_principal_id = save_files(imagen=logo_principal_file)
        logo_secundario_id = save_files(imagen=logo_secundario_file)
    except Exception as e:
        return jsonify({"message": "Error al leer los archivos adjuntos: {}".format(str(e))}), 500

    personalizacion_collection.insert_one({
        "nombre_restaurante": nombre_restaurante,
        "logo_principal": logo_principal_id,
        "logo_secundario": logo_secundario_id
    })

    return jsonify({"message": "Información de personalización creada correctamente"}), 201


#3.5. Sacar unicamente el primer id de nuestra tabla que es la que usaremos para modificar todo. 
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


#--------------------------------------------------------------------------------------------------------------------------------------#
#                                   4.Pedidos de los clientes

pedidos_collection = client_db["tickets"]  #


##Obtener la lista de pedidos 
@app.route("/pedidos", methods=["GET"])
def get_pedidos():
    pedidos = pedidos_collection.find()
    if pedidos:
        return jsonify(json_util.dumps(pedidos)), 200
    else:
        return jsonify({"message":"No se encontró ningún pedido"}), 404


@app.route("/pedidos/<id>", methods=["DELETE"])
def delete_pedido(id):
    pedido = pedidos_collection.find_one({"_id": ObjectId(id)})
    if pedido:
        pedidos_collection.delete_one({"_id": ObjectId(id)})
        return jsonify({"message":"Pedido borrado correctamente"}), 200
    else:
        return jsonify({"message":"Pedido no encontrado"}), 404
    


@app.route("/pedidos", methods=["POST"])
def add_pedido():
    info = request.get_json()
    
    if info:
        pedido_id = pedidos_collection.insert_one(info).inserted_id
        return jsonify({"message": "Pedido agregado correctamente", "_id": str(pedido_id)}), 201
    else:
        return jsonify({"message":"Error en la solicitud"}), 400



if __name__ == "__main__":
    app.run(debug=True)





