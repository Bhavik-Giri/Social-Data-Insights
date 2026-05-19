"""
data_cleaner.py
---------------
Cleans the parsed profile data.
Removes failed parses, deduplicates usernames,
and strips any profiles with missing critical fields.
"""

def clean_profiles(profiles):
    """
    Cleans a list of parsed profile dictionaries.

    Steps:
        1. Remove None entries (failed parses)
        2. Remove duplicate usernames (keep first occurrence)
        3. Remove profiles missing username or name

    Args:
        profiles (list): Output from parse_all().

    Returns:
        list: Cleaned list of profile dicts.
    """
    # Remove None entries
    profiles = [p for p in profiles if p is not None]

    # Remove profiles with missing critical fields
    profiles = [p for p in profiles if p.get("username") and p.get("name")]

    # Deduplicate by username (keep first occurrence)
    seen = set()
    unique_profiles = []
    for p in profiles:
        if p["username"] not in seen:
            seen.add(p["username"])
            unique_profiles.append(p)

    return unique_profiles