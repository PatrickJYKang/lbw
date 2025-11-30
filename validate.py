import json
import sys
from jsonschema import validate, ValidationError

def main():
    if len(sys.argv) != 2:
        print("Usage: python validate.py <datafile.json>")
        sys.exit(1)

    data_path = sys.argv[1]
    schema_path = "lbw_schema.json"

    try:
        with open(schema_path, "r") as f:
            schema = json.load(f)
    except FileNotFoundError:
        print(f"Schema file not found: {schema_path}")
        sys.exit(1)

    try:
        with open(data_path, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Data file not found: {data_path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in data file: {e}")
        sys.exit(1)

    try:
        validate(instance=data, schema=schema)
        print("Valid!")
    except ValidationError as e:
        print("Validation error:")
        print(e.message)
        print("\nLocation:", list(e.path))
        sys.exit(1)

if __name__ == "__main__":
    main()
