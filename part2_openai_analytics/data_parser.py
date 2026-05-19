"""
data_parser.py
--------------
Parses raw profile text chunks into structured Python dictionaries.
Handles K (thousands) and M (millions) in follower/following counts.
"""

def parse_chunk(chunk):
    """
    Parses a single raw profile text block into a structured dictionary.

    Args:
        chunk (str): A raw multi-line string for one profile.

    Returns:
        dict or None: Parsed profile data, or None if parsing fails.

    Output dict keys:
        username, no_of_posts, no_of_followers,
        no_of_following, name, type_of_page, bio
    """
    try:
        chunk = chunk.strip()
        sep_chunk = chunk.split('\n')

        username = sep_chunk[0]

        # Parse posts (e.g. "420 posts" → 420)
        no_of_posts = int(sep_chunk[1].split(" post")[0].replace(",", ""))

        # Parse followers — handles K and M suffixes
        followers_raw = sep_chunk[2]
        no_of_followers = float(
            followers_raw.split(" follower")[0]
            .replace(",", "").replace("K", "").replace("M", "")
        )
        if "K" in followers_raw:
            no_of_followers = int(no_of_followers * 1000)
        elif "M" in followers_raw:
            no_of_followers = int(no_of_followers * 1000000)
        else:
            no_of_followers = int(no_of_followers)

        # Parse following — handles K and M suffixes
        following_raw = sep_chunk[3]
        no_of_following = float(
            following_raw.split(" following")[0]
            .replace(",", "").replace("K", "").replace("M", "")
        )
        if "K" in following_raw:
            no_of_following = int(no_of_following * 1000)
        elif "M" in following_raw:
            no_of_following = int(no_of_following * 1000000)
        else:
            no_of_following = int(no_of_following)

        name = sep_chunk[4]

        # Category and bio are optional fields
        if len(sep_chunk) > 5:
            type_of_page = sep_chunk[5]
            bio = "\n".join(sep_chunk[6:])
        else:
            type_of_page = "Unknown"
            bio = ""

        return {
            "username": username,
            "no_of_posts": no_of_posts,
            "no_of_followers": no_of_followers,
            "no_of_following": no_of_following,
            "name": name,
            "type_of_page": type_of_page,
            "bio": bio
        }

    except Exception:
        return None  # Skip malformed profiles


def parse_all(chunks):
    """
    Parses all raw chunks into a list of profile dictionaries.

    Args:
        chunks (list): List of raw string chunks from load_raw_data().

    Returns:
        list: List of successfully parsed profile dicts.
    """
    all_profiles = []
    for chunk in chunks:
        parsed = parse_chunk(chunk)
        if parsed:
            all_profiles.append(parsed)
    return all_profiles