# validate_truth_trace.py
import json
import jsonschema
import hashlib

def validate(fact: dict) -> bool:
    with open("schema.json") as f:
        schema = json.load(f)
    jsonschema.validate(fact, schema)
    # verify hash
    payload = f"{fact['claim']}-{fact['source_endpoint']}-{fact['timestamp']}"
    expected = hashlib.sha256(payload.encode()).hexdigest()
    return fact['integrity_hash'] == expected
