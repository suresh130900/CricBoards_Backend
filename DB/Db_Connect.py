from pymongo import MongoClient
from pymongo import errors


def db_connection():
    try:
        client = MongoClient("localhost",27017)
        db = client.get_database("ipl")
        print("CONNECTION SUCESSFULL")
        return db

    except errors.PyMongoError:
        print("CONNECTION ERROR")
