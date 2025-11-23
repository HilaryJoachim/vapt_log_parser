from db.mongo_client import get_mongo_client

def test():
    try:
        client = get_mongo_client()
        db = client["vapt_db"]
        col = db["test_collection"]

        result = col.insert_one({"status": "connected"})
        print("Inserted:", result.inserted_id)

        doc = col.find_one({"_id": result.inserted_id})
        print("Document:", doc)

        print("MongoDB test successful")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    test()
