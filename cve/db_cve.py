# vapt_parser/cve/db_cve.py
from db.mongo_client import get_mongo_client

client = get_mongo_client()
db = client["vapt_cve"]

# CVE collections
cve_items = db["cve_items"]
cve_metadata = db["cve_metadata"]
cpe_match = db["cpe_match"]

def save_cve_item(item):
    """Upsert CVE entry based on CVE ID."""
    cve_id = item.get("cve_id")
    if not cve_id:
        return None

    result = cve_items.update_one(
        {"cve_id": cve_id},
        {"$set": item},
        upsert=True
    )
    return result
