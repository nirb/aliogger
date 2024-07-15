from pymongo.mongo_client import MongoClient
from bson.objectid import ObjectId
from pymongo.server_api import ServerApi
import os 

class DbApi:
    def __init__(self) -> None:
        self.client = None

    def __del__(self) -> None:
        if self.client:
            self.client.close()
            print("DbApi - closing client")

    def init(self, database_name):
        if self.connect():
            self.create_database_if_not_exists(database_name)

    def insert_document(self,db_name,collection_name, document)->int:
        print(f"insert_document {db_name=} {collection_name=} {document=}")
        db = self.client[db_name]
        collection = db[collection_name]
        existing_doc = collection.find_one({"name": document["name"]})  
    
        if existing_doc is None:
            insert_result = collection.insert_one(document)
            print(f"Inserted document with ID: {insert_result.inserted_id}")
            return 0
        else:
            print("Document already exists. Skipping insertion.")
            return -1
        
    def delete_document(self,db_name,collection_name,document_id):
        query_filter = { "_id":ObjectId(document_id) }
        db = self.client[db_name]
        collection = db[collection_name]
        result = collection.delete_one(query_filter)
        print("delete_document count",result.deleted_count)
        return 0 if result.deleted_count == 1 else -1

        
    def get_collection(self,db_name,collection_name):
        print(f"get_collection {db_name=} {collection_name=}")
        db = self.client[db_name]
        items=  []
        for item in db[collection_name].find():
            items.append(item)
        return items

    def connect(self):
        # Create a new client and connect to the server
        print("DbApi connecting",os.getenv("MONGO_URI"))
        client = MongoClient(os.getenv("MONGO_URI"), server_api=ServerApi('1'))
        # Send a ping to confirm a successful connection
        try:
            client.admin.command('ping')
            self.client = client
            print("Pinged your deployment. You successfully connected to MongoDB!")
            return self.client
        except Exception as e:
            print(f"Error connecting to db {e}")
            return None

    def create_database_if_not_exists(self, database_name):
        db_list = self.client.list_database_names()
        if database_name not in db_list:
            print(f"Database '{database_name}' does not exist. Creating it...")
            self.client[database_name].command("ping")  # Create the database by sending a ping command
            print(f"Database '{database_name}' created successfully.")
