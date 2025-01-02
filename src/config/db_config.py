from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection

class PyMongoConnector:
    def __init__(self):
        pass

    @property
    def client(self) -> MongoClient:
        uri: str = 'mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.2.6'
        return MongoClient(uri)

    def get_database(self, db_name: str) -> Database:
        return self.client.get_database(db_name)

    def get_collection(self, db_name: str, col_name: str) -> Collection:
        return self.get_database(db_name).get_collection(col_name)