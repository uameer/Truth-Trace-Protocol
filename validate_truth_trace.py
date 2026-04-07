import json
import jsonschema
import hashlib
import sys


def validate(fact: dict) -> bool:
    """Validate a Truth-Trace fact against schema and verify integrity hash."""
    # Step 1: Schema validation
    with open("schema.json") as f:
        schema = json.load(f)
    jsonschema.validate(fact, schema)

    # Step 2: Integrity hash verification
    payload = f"{fact['claim']}-{fact['source_endpoint']}-{fact['timestamp']}"
    expected = hashlib.sha256(payload.encode()).hexdigest()
    return fact['integrity_hash'] == expected


def generate_hash(claim: str, source_endpoint: str, timestamp: str) -> str:
    """Generate a valid integrity hash for a new Truth-Trace fact."""
    payload = f"{claim}-{source_endpoint}-{timestamp}"
    return hashlib.sha256(payload.encode()).hexdigest()


if __name__ == "__main__":
    # Example fact — replace with real data
    example_fact = {
        "claim": "Patient requires Lumbar MRI based on neurological red flags.",
        "provenance_type": "Human_Audit",
        "source_endpoint": "https://ehr.example.com/records/patient-001",
        "timestamp": "2026-04-07T21:00:00Z",
        "model_uncertainty": 0.12,
        "integrity_hash": ""  # generated below
    }

    # Generate hash for the example
    example_fact["integrity_hash"] = generate_hash(
        example_fact["claim"],
        example_fact["source_endpoint"],
        example_fact["timestamp"]
    )

    # Validate
    try:
        result = validate(example_fact)
        print(f"✅ Valid Truth-Trace fact: {result}")
        print(f"Hash: {example_fact['integrity_hash']}")
    except jsonschema.ValidationError as e:
        print(f"❌ Schema validation failed: {e.message}")
    except Exception as e:
        print(f"❌ Error: {e}")
