from pymongo import MongoClient


def connect_db():
    client = MongoClient("localhost", 27017)
    db = client["Cafeteria"]
    return db
