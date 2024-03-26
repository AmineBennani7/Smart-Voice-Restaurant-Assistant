from flask import Flask, jsonify, request
from pymongo import MongoClient
from config import Config 
from flask_cors import CORS
from bson import ObjectId

from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity



app = Flask(__name__)
CORS(app)  # Habilitar CORS para toda la aplicación (usar flask en varios puertos del localhost)




app.config.from_object(Config) #carpeta Config contiene  Clave secreta para firmar el token JWT
jwt = JWTManager(app)

client = MongoClient("mongodb://localhost:27017/")
database = client["menu"]  
usuarios_collection = database["usuarios"] 


##REGISTRACION 
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

#Connect
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


##Tabla de todos los users
@app.route("/users", methods=["GET"])
def get_users():
    users = usuarios_collection.find()
    result = []
    for user in users:
        user["_id"] = str(user["_id"])  # Convertir el objeto id de Mongo en una cadena
        result.append(user)
    return jsonify(result)

##Borrar user específico: 
@app.route("/user/<userid>", methods=["DELETE"])
def delete_user(userid): 
    response = usuarios_collection.delete_one({"_id": ObjectId(userid)})
    
    if response.deleted_count:
        return jsonify({"message": "Usuario borrado correctamente"}), 200

    return jsonify({"message": "Usuario no encontrado"}), 404

if __name__ == "__main__":
    app.run(debug=True)
  