from flask import Flask, request, jsonify
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId
from flask_cors import CORS
from pymongo.server_api import ServerApi

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = '2311'

# Configuración de MongoDB
uri = "mongodb+srv://greg:2311@app.myezwki.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri, server_api=ServerApi('1'))

db = client['app']
users_collection = db['users']
tasks_collection = db['tasks']

@app.route('/register', methods=['POST'])
def register():
    username = request.json['username']
    password = request.json['password']
    existing_user = users_collection.find_one({'username': username})

    if existing_user is None:
        hashed_password = generate_password_hash(password)
        users_collection.insert_one({'username': username, 'password': hashed_password})
        print(f"Nuevo usuario registrado: {username}")
        return jsonify({'message': 'User registered successfully'}), 201
    else:
        print(f"Intento de registro fallido para el usuario: {username}, el usuario ya existe.")
        return jsonify({'message': 'User already exists'}), 409

@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    user = users_collection.find_one({'username': username})

    if user:
        if check_password_hash(user['password'], password):
            print(f"Usuario {username} ha iniciado sesión con éxito.")
            return jsonify({'message': 'Login successful'}), 200
        else:
            print(f"Usuario {username} ha fallado en el inicio de sesión. Contraseña incorrecta.")
    else:
        print(f"Usuario {username} no encontrado durante el intento de inicio de sesión.")

    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/tasks', methods=['POST'])
def add_task():
    username = request.json['usuario']
    title = request.json['título']
    tasks_collection.insert_one({'usuario': username, 'título': title, 'completada': False})
    print(f"Usuario {username} ha añadido una nueva tarea: {title}")
    return jsonify({'message': 'Task added successfully'}), 201

@app.route('/tasks', methods=['GET'])
def get_tasks():
    username = request.args.get('usuario')
    user_tasks = tasks_collection.find({'usuario': username})
    print(f"Recuperando tareas para el usuario: {username}")
    return jsonify(list(user_tasks)), 200

@app.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    result = tasks_collection.delete_one({'_id': ObjectId(task_id)})
    if result.deleted_count:
        print(f"Tarea con ID {task_id} ha sido eliminada.")
        return jsonify({'message': 'Task deleted successfully'}), 200
    else:
        print(f"No se encontró la tarea con ID {task_id} para eliminar.")
        return jsonify({'message': 'Task not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
