# Reads your MongoDB connection string from .env
# #Connects to vapt_logs db
# Writes normalized logs to normalized_logs collection

from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()  # Load .env file

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["vapt_logs"]        # database
normalized_collection = db["normalized_logs"]   # collection


def save_log(document: dict):
    """Insert normalized log into MongoDB"""
    result = normalized_collection.insert_one(document)
    return str(result.inserted_id)
