"""
insights.py
-----------
Extracts meaningful insights from cleaned Instagram profile data.

Answers:
    1. Who has the maximum posts?
    2. Who has the maximum followers?
    3. Who follows the maximum people?
    4. How many categories exist, and how many per category?
"""

def max_posts(profiles):
    """Returns the profile with the most posts."""
    return max(profiles, key=lambda x: x['no_of_posts'])


def max_followers(profiles):
    """Returns the profile with the most followers."""
    return max(profiles, key=lambda x: x['no_of_followers'])


def max_following(profiles):
    """Returns the profile that follows the most people."""
    return max(profiles, key=lambda x: x['no_of_following'])


def category_breakdown(profiles):
    """
    Returns a dictionary of all categories and their counts,
    sorted from most common to least.

    Returns:
        dict: {category_name: count} sorted descending
    """
    categories = {}
    for p in profiles:
        cat = p['type_of_page']
        categories[cat] = categories.get(cat, 0) + 1
    return dict(sorted(categories.items(), key=lambda x: x[1], reverse=True))


def print_insights(profiles):
    """Prints all 4 insights in a clean, readable format."""
    print("=" * 50)
    print("  INSIGHTS: CODERS OF BANGALORE")
    print("=" * 50)

    mp = max_posts(profiles)
    print(f"\n📸 Max Posts:     @{mp['username']} — {mp['no_of_posts']} posts")

    mf = max_followers(profiles)
    print(f"👥 Max Followers: @{mf['username']} — {mf['no_of_followers']:,} followers")

    mfg = max_following(profiles)
    print(f"🔁 Max Following: @{mfg['username']} — {mfg['no_of_following']} following")

    cats = category_breakdown(profiles)
    print(f"\n🏷️  Total Categories: {len(cats)}")
    print("\n  Category Breakdown:")
    for cat, count in cats.items():
        print(f"    {cat:<30} → {count} account(s)")