from .mongo_client import get_mongo_client


def save_log(document: dict):
	"""Insert normalized log into MongoDB using package mongo client."""
	client = get_mongo_client()
	db = client["vapt_db"]
	normalized_collection = db["normalized_logs"]
	result = normalized_collection.insert_one(document)
	return str(result.inserted_id)
