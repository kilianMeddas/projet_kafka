import os
from pymongo import MongoClient

# Get MongoDB URI from environment variable
def connect_to_db():
    mongo_uri = os.getenv('MONGO_URI', 'mongodb://mongo:27017') 
    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
    db = client['caisse']
    #tickets = db['shop']

    print("Connectd to MongoDB successfully")

    return db
