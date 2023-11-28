from flask import Flask, request, jsonify
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId
from flask_cors import CORS
from pymongo.server_api import ServerApi

# Inicializar la aplicación Flask y habilitar CORS
app = Flask(__name__)
CORS(app)
# Clave secreta de la aplicación para mantener la seguridad de las sesiones
app.config['SECRET_KEY'] = '2311'

# Conectar a la base de datos MongoDB utilizando la URI proporcionada
client = MongoClient(
    "mongodb+srv://greg:2311@app.myezwki.mongodb.net/?retryWrites=true&w=majority",
    server_api=ServerApi('1')
)
db = client['app']
users_collection = db['users']
tasks_collection = db['tasks']

# Endpoint para registrar nuevos usuarios
@app.route('/register', methods=['POST'])
def register():
    # Obtener el nombre de usuario y la contraseña de la solicitud
    username = request.json['username']
    password = request.json['password']
    # Verificar si el usuario ya existe en la base de datos
    existing_user = users_collection.find_one({'username': username})

    # Si el usuario no existe, registrar un nuevo usuario
    if existing_user is None:
        hashed_password = generate_password_hash(password)
        users_collection.insert_one({'username': username, 'password': hashed_password})
        return jsonify({'message': 'User registered successfully'}), 201
    else:
        return jsonify({'message': 'User already exists'}), 409

# Endpoint para iniciar sesión de usuarios
@app.route('/login', methods=['POST'])
def login():
    # Obtener el nombre de usuario y la contraseña de la solicitud
    username = request.json['username']
    password = request.json['password']
    # Buscar el usuario en la base de datos
    user = users_collection.find_one({'username': username})

    # Verificar la contraseña y responder si es correcta o no
    if user and check_password_hash(user['password'], password):
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

# Endpoint para añadir tareas
@app.route('/tasks', methods=['POST'])
def add_task():
    # Obtener el nombre de usuario y el título de la tarea de la solicitud
    username = request.json['usuario']
    title = request.json['título']
    # Insertar la nueva tarea en la base de datos
    result = tasks_collection.insert_one({'usuario': username, 'título': title, 'completada': False})
    return jsonify({'message': 'Task added successfully', 'task_id': str(result.inserted_id)}), 201

# Endpoint para obtener las tareas de un usuario
@app.route('/tasks', methods=['GET'])
def get_tasks():
    # Obtener el nombre de usuario de la solicitud
    username = request.args.get('usuario')
    # Buscar las tareas del usuario en la base de datos
    user_tasks = tasks_collection.find({'usuario': username})
    # Convertir las tareas a una lista y asegurarse de que los ObjectId sean serializables
    tasks_list = [{'_id': str(task['_id']), 'título': task['título'], 'completada': task['completada']} for task in user_tasks]
    return jsonify(tasks_list), 200

# Endpoint para eliminar una tarea específica
@app.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    # Eliminar la tarea por su ID
    result = tasks_collection.delete_one({'_id': ObjectId(task_id)})
    if result.deleted_count:
        return jsonify({'message': 'Task deleted successfully'}), 200
    else:
        return jsonify({'message': 'Task not found'}), 404

# Endpoint para actualizar el estado de una tarea
@app.route('/tasks/<task_id>', methods=['PATCH'])
def update_task(task_id):
    # Obtener el estado 'completado' de la solicitud
    completed = request.json['completed']
    # Actualizar el estado de la tarea en la base de datos
    result = tasks_collection.update_one({'_id': ObjectId(task_id)}, {'$set': {'completada': completed}})
    if result.modified_count:
        return jsonify({'message': 'Task updated successfully'}), 200
    else:
        return jsonify({'message': 'No changes made to the task'}), 200


# Endpoint para actualizar una tarea
@app.route('/tasks/<task_id>', methods=['PUT'])
def edit_task(task_id):
    # Se espera que el cuerpo de la solicitud contenga un campo 'título'
    new_title = request.json['título']
    try:
        result = tasks_collection.update_one(
            {'_id': ObjectId(task_id)},
            {'$set': {'título': new_title}}
        )
        if result.modified_count:
            return jsonify({'message': 'Task updated successfully'}), 200
        else:
            return jsonify({'message': 'No changes made to the task or task not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ejecutar la aplicación Flask si el archivo es el programa principal
if __name__ == '__main__':
    app.run(debug=True)