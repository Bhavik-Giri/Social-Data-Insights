def find_pages_you_might_like(user_id, data, top_n=5):
    """
    Suggests pages the user might like based on shared interests with others.
    Pages liked by users who share common liked pages get higher scores.

    Args:
        user_id (int): The ID of the user to find page suggestions for.
        data (dict): The loaded social network data.
        top_n (int): Number of top recommendations to return. Default is 5.

    Returns:
        list of tuples: [(page_id, score), ...] sorted by score descending.
    """
    # Build a map: user_id -> set of liked pages
    user_pages = {}
    for user in data["users"]:
        user_pages[user["id"]] = set(user["liked_pages"])

    if user_id not in user_pages:
        return []

    user_liked_pages = user_pages[user_id]
    page_suggestion = {}

    for other_user, pages in user_pages.items():
        if other_user != user_id:
            shared_pages = user_liked_pages.intersection(pages)

            # Only recommend if at least 1 shared page exists
            if shared_pages:
                for page in pages:
                    if page not in user_liked_pages:
                        page_suggestion[page] = page_suggestion.get(page, 0) + len(shared_pages)

    sorted_pages = sorted(page_suggestion.items(), key=lambda x: x[1], reverse=True)
    return [(page_id, score) for page_id, score in sorted_pages][:top_n]