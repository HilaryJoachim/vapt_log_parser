# vapt_parser/db/mongo_client.py
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()

import os

def get_mongo_client():
    # Load password from environment variable
    password = os.getenv("VAPT_DB_PASSWORD")
    if not password:
        raise ValueError("❌ Missing environment variable: VAPT_DB_PASSWORD")

    # Build MongoDB Atlas connection URI
    uri = (
        f"mongodb+srv://vapt_user:Lhm8Iopavo1e6Pkh"
        "@vaptcluster.dejko6v.mongodb.net/vapt_db"
        "?retryWrites=true&w=majority&tls=true"
    )

    client = MongoClient(uri)
    return client
