from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


def connect_db():
    try:
        client = MongoClient("localhost", 27017, serverSelectionTimeoutMS=5000)
        db = client["Cafeteria"]
        client.server_info()
        return db
    except ConnectionFailure as e:
        print(f"Failed to connect to the database: {e}")
        return None
