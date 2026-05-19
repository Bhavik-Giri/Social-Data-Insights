import json

def load_data(filename):
    """Load JSON data from a file."""
    with open(filename, "r") as f:
        return json.load(f)