from pymongo import MongoClient
from pymongo.server_api import ServerApi

# Reemplaza con tu URI de MongoDB
uri = "mongodb+srv://greg:2311@app.myezwki.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri, server_api=ServerApi('1'))

# Reemplaza con el nombre de tu base de datos
db = client["app"]

# Intenta obtener el nombre de las colecciones
try:
    collections = db.list_collection_names()
    print("Colecciones en la base de datos:", collections)
except Exception as e:
    print("Error al conectar a MongoDB:", e)
