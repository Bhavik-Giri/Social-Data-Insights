import json

def clean_data(data):
    """
    Cleans raw social network data:
    - Removes users with missing names
    - Removes duplicate friends
    - Removes inactive users (no friends & no liked pages)
    - Removes duplicate pages
    """
    # Remove users with missing names
    data["users"] = [user for user in data["users"] if user["name"].strip()]

    # Remove duplicate friends
    for user in data["users"]:
        user["friends"] = list(set(user["friends"]))

    # Remove inactive users
    data["users"] = [user for user in data["users"] if user["friends"] or user["liked_pages"]]

    # Remove duplicate pages (keeps last entry for duplicate IDs)
    unique_pages = {}
    for page in data["pages"]:
        unique_pages[page["id"]] = page
    data["pages"] = list(unique_pages.values())

    return data