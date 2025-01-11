from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

uri = f"mongodb+srv://crimtrajano:dFSzATRLjzEXBCE6@globehackathon.t8zsy.mongodb.net/?retryWrites=true&w=majority&appName=Globehackathon"

client = MongoClient(uri)

db = client["globehackathon"]
collection = db["tweets_data"]


def UploadToMongoDB(_item):
    print("Uploading!!", str(_item)[:25])
    result = collection.insert_many(_item)
    print("Inserted IDs:", result.inserted_ids)
