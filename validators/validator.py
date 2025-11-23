# src/validator.py
import json
from jsonschema import Draft7Validator, FormatChecker
from dateutil import parser as dtparser
from pathlib import Path

SCHEMA_PATH = Path(__file__).resolve().parents[1] / "schemas" / "normalized_schema.json"

def load_schema():
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def normalize_timestamp(value):
    # Accept many formats, return ISO 8601 with timezone if possible
    dt = dtparser.parse(value)
    return dt.isoformat()

def validate_and_prepare(raw_doc):
    schema = load_schema()
    validator = Draft7Validator(schema, format_checker=FormatChecker())
    doc = raw_doc.copy()

    # Ensure timestamp is ISO string
    if "timestamp" in doc:
        try:
            doc["timestamp"] = normalize_timestamp(doc["timestamp"])
        except Exception as e:
            raise ValueError(f"Invalid timestamp: {doc.get('timestamp')} -> {e}")

    errors = sorted(validator.iter_errors(doc), key=lambda e: e.path)
    if errors:
        msgs = []
        for e in errors:
            path = ".".join(map(str, list(e.path))) or "(root)"
            msgs.append(f"{path}: {e.message}")
        raise ValueError("Schema validation errors: " + "; ".join(msgs))
    
    return doc  



# Simple test when run as main

if __name__ == "__main__":
    test_log = {
        "timestamp": "2025-11-10 15:30:00",
        "host": "ServerX",
        "os": "Ubuntu",
        "software": "Apache",
        "version": "2.4.29",
        "event_type": "service_start",
        "message": "Started Apache/2.4.29 (Ubuntu)",
        "source": "syslog"
    }

    try:
        result = validate_and_prepare(test_log)
        print("VALIDATED:", result)
    except Exception as e:
        print("ERROR:", e)
