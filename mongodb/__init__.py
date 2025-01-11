import sys
from pymongo import MongoClient

sys.path.append("/Users/chrismanueltrajano/Documents/Github/hacktathons/konektado-api")

uri = f"mongodb+srv://crimtrajano:zGlTax2n48zT5iL9@globehackathon.t8zsy.mongodb.net/?retryWrites=true&w=majority&appName=Globehackathon"
client = MongoClient(uri, ssl=True)

db = client["globehackathon"]
collection = db["tweets_data"]


def UploadToMongoDB(_item):
    # Ensure _item is a list
    if not isinstance(_item, list):
        raise ValueError("Expected _item to be a list of documents.")

    # Print the items being uploaded
    print("Uploading items:", _item)

    # Insert the items into the collection
    result = collection.insert_many(_item)

    # Convert inserted ObjectIds to strings for readability
    inserted_ids = [str(inserted_id) for inserted_id in result.inserted_ids]

    # Print the inserted IDs
    print("Inserted IDs:", inserted_ids)
