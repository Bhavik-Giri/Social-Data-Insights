def find_people_you_may_know(user_id, data):
    """
    Suggests people the user may know based on mutual friends.
    More mutual friends = higher priority in the suggestion.

    Args:
        user_id (int): The ID of the user to find suggestions for.
        data (dict): The loaded social network data.

    Returns:
        list: Sorted list of suggested user IDs.
    """
    # Build a map: user_id -> set of their friends
    user_friends = {}
    for user in data["users"]:
        user_friends[user["id"]] = set(user["friends"])

    if user_id not in user_friends:
        return []

    direct_friends = user_friends[user_id]
    suggestions = {}

    for friend in direct_friends:
        for mutual in user_friends[friend]:
            # Must not be the user themselves or already a direct friend
            if mutual != user_id and mutual not in direct_friends:
                suggestions[mutual] = suggestions.get(mutual, 0) + 1

    # Sort by number of mutual friends (highest first)
    sorted_suggestions = sorted(suggestions.items(), key=lambda x: x[1], reverse=True)
    return [uid for uid, count in sorted_suggestions]