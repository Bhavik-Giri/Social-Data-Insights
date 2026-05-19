"""
data_collector.py
-----------------
Documents the data collection process for the Coders of Bangalore dataset.

HOW THE DATA WAS COLLECTED:
- Source: Instagram profiles of OpenAI followers (Bangalore tech community)
- Method: Manual data collection from Instagram profiles
- Total profiles collected: 107
- Format: Each profile stored as a text block separated by double newlines (\n\n)

Each block follows this structure:
    username
    X posts
    X followers
    X following
    Full Name
    Category (optional)
    Bio lines (optional)

Files:
    - initialdata.txt  → 13 profiles (sample/testing data)
    - finaldata.txt    → 107 profiles (main dataset)
"""

def load_raw_data(filepath):
    """
    Reads the raw text file and splits it into individual profile chunks.

    Args:
        filepath (str): Path to the raw .txt data file.

    Returns:
        list: List of raw string chunks, one per profile.
    """
    with open(filepath, encoding='utf-8') as f:
        data = f.read()

    chunks = data.split("\n\n")
    chunks = [c for c in chunks if len(c) > 3]  # Remove empty/junk blocks
    return chunks