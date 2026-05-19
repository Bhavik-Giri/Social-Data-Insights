"""
╔══════════════════════════════════════════════════════════════╗
║              SocialScope — Social Data Insights              ║
║                                                              ║
║  Part 1 → CodeBook Recommendation Engine (pure Python)       ║
║  Part 2 → Coders of Bangalore Instagram Analytics            ║
║                                                              ║
║  Author  : Your Name                                         ║
║  Language: Pure Python (no pandas, no NumPy)                 ║
╚══════════════════════════════════════════════════════════════╝
"""

import json
import os

# ─────────────────────────────────────────────
#  PART 1 — HELPER FUNCTIONS
# ─────────────────────────────────────────────

def load_json(filepath):
    """Load JSON data from a file."""
    with open(filepath, "r") as f:
        return json.load(f)


def clean_data(data):
    """
    Cleans raw CodeBook social network data.
    - Removes users with missing names
    - Removes duplicate friends
    - Removes inactive users (no friends & no liked pages)
    - Removes duplicate pages
    """
    data["users"] = [user for user in data["users"] if user["name"].strip()]

    for user in data["users"]:
        user["friends"] = list(set(user["friends"]))

    data["users"] = [
        user for user in data["users"]
        if user["friends"] or user["liked_pages"]
    ]

    unique_pages = {}
    for page in data["pages"]:
        unique_pages[page["id"]] = page
    data["pages"] = list(unique_pages.values())

    return data


def find_people_you_may_know(user_id, data):
    """
    Suggests people the user may know based on mutual friends.
    Higher mutual friends = higher priority recommendation.
    """
    user_friends = {}
    for user in data["users"]:
        user_friends[user["id"]] = set(user["friends"])

    if user_id not in user_friends:
        return []

    direct_friends = user_friends[user_id]
    suggestions = {}

    for friend in direct_friends:
        for mutual in user_friends[friend]:
            if mutual != user_id and mutual not in direct_friends:
                suggestions[mutual] = suggestions.get(mutual, 0) + 1

    sorted_suggestions = sorted(
        suggestions.items(), key=lambda x: x[1], reverse=True
    )
    return [uid for uid, count in sorted_suggestions]


def find_pages_you_might_like(user_id, data, top_n=5):
    """
    Suggests pages the user might like based on shared interests.
    Pages liked by users who share common pages score higher.
    """
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
            if shared_pages:
                for page in pages:
                    if page not in user_liked_pages:
                        page_suggestion[page] = (
                            page_suggestion.get(page, 0) + len(shared_pages)
                        )

    sorted_pages = sorted(
        page_suggestion.items(), key=lambda x: x[1], reverse=True
    )
    return [(page_id, score) for page_id, score in sorted_pages][:top_n]


# ─────────────────────────────────────────────
#  PART 2 — HELPER FUNCTIONS
# ─────────────────────────────────────────────

def load_raw_text(filepath):
    """Reads raw .txt file and splits into individual profile chunks."""
    with open(filepath, encoding="utf-8") as f:
        data = f.read()
    chunks = data.split("\n\n")
    return [c for c in chunks if len(c) > 3]


def parse_chunk(chunk):
    """
    Parses a single raw Instagram profile block into a dictionary.
    Handles K (thousands) and M (millions) in counts.
    Returns None if parsing fails (malformed data).
    """
    try:
        chunk = chunk.strip()
        lines = chunk.split("\n")

        username = lines[0]

        no_of_posts = int(lines[1].split(" post")[0].replace(",", ""))

        followers_raw = lines[2]
        no_of_followers = float(
            followers_raw.split(" follower")[0]
            .replace(",", "").replace("K", "").replace("M", "")
        )
        if "K" in followers_raw:
            no_of_followers = int(no_of_followers * 1000)
        elif "M" in followers_raw:
            no_of_followers = int(no_of_followers * 1_000_000)
        else:
            no_of_followers = int(no_of_followers)

        following_raw = lines[3]
        no_of_following = float(
            following_raw.split(" following")[0]
            .replace(",", "").replace("K", "").replace("M", "")
        )
        if "K" in following_raw:
            no_of_following = int(no_of_following * 1000)
        elif "M" in following_raw:
            no_of_following = int(no_of_following * 1_000_000)
        else:
            no_of_following = int(no_of_following)

        name = lines[4]

        if len(lines) > 5:
            type_of_page = lines[5]
            bio = "\n".join(lines[6:])
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
            "bio": bio,
        }

    except Exception:
        return None


def clean_profiles(profiles):
    """
    Cleans parsed Instagram profiles.
    - Removes failed/None parses
    - Removes profiles with missing username or name
    - Deduplicates by username (keeps first occurrence)
    """
    profiles = [p for p in profiles if p is not None]
    profiles = [p for p in profiles if p.get("username") and p.get("name")]

    seen = set()
    unique = []
    for p in profiles:
        if p["username"] not in seen:
            seen.add(p["username"])
            unique.append(p)
    return unique


def get_max_posts(profiles):
    return max(profiles, key=lambda x: x["no_of_posts"])


def get_max_followers(profiles):
    return max(profiles, key=lambda x: x["no_of_followers"])


def get_max_following(profiles):
    return max(profiles, key=lambda x: x["no_of_following"])


def get_category_breakdown(profiles):
    categories = {}
    for p in profiles:
        cat = p["type_of_page"]
        categories[cat] = categories.get(cat, 0) + 1
    return dict(sorted(categories.items(), key=lambda x: x[1], reverse=True))


# ─────────────────────────────────────────────
#  RUNNER FUNCTIONS
# ─────────────────────────────────────────────

def run_part1():
    print("\n" + "═" * 60)
    print("   PART 1 — CODEBOOK RECOMMENDATION ENGINE")
    print("   (People You May Know  +  Pages You Might Like)")
    print("═" * 60)

    # ── Load & Clean ──
    data_path = os.path.join("data", "massive_data.json")
    if not os.path.exists(data_path):
        print(f"\n  [ERROR] File not found: {data_path}")
        print("  Make sure massive_data.json is inside the data/ folder.\n")
        return

    data = load_json(data_path)
    data = clean_data(data)

    id_to_name = {u["id"]: u["name"] for u in data["users"]}
    id_to_page = {p["id"]: p["name"] for p in data["pages"]}

    print(f"\n  ✅ Data loaded — {len(data['users'])} users | {len(data['pages'])} pages")

    # ── People You May Know ──
    print("\n" + "─" * 60)
    print("  👥  PEOPLE YOU MAY KNOW")
    print("─" * 60)

    test_users = [1, 5, 10]
    for uid in test_users:
        user_name = id_to_name.get(uid, f"User {uid}")
        suggestions = find_people_you_may_know(uid, data)
        suggestion_names = [id_to_name.get(s, str(s)) for s in suggestions[:5]]
        print(f"\n  @{user_name} (ID {uid}) — You may know:")
        if suggestion_names:
            for i, name in enumerate(suggestion_names, 1):
                print(f"    {i}. {name}")
        else:
            print("    No suggestions found.")

    # ── Pages You Might Like ──
    print("\n" + "─" * 60)
    print("  📄  PAGES YOU MIGHT LIKE")
    print("─" * 60)

    for uid in test_users:
        user_name = id_to_name.get(uid, f"User {uid}")
        page_recs = find_pages_you_might_like(uid, data, top_n=3)
        print(f"\n  @{user_name} (ID {uid}) — Recommended pages:")
        if page_recs:
            for i, (page_id, score) in enumerate(page_recs, 1):
                page_name = id_to_page.get(page_id, f"Page {page_id}")
                print(f"    {i}. {page_name}  (score: {score})")
        else:
            print("    No page recommendations found.")


def run_part2():
    print("\n\n" + "═" * 60)
    print("   PART 2 — CODERS OF BANGALORE: INSTAGRAM ANALYTICS")
    print("   (Data Collection → Parsing → Cleaning → Insights)")
    print("═" * 60)

    data_path = os.path.join("data", "finaldata.txt")
    if not os.path.exists(data_path):
        print(f"\n  [ERROR] File not found: {data_path}")
        print("  Make sure finaldata.txt is inside the data/ folder.\n")
        return

    # ── Step 1: Collect / Load ──
    print("\n  📦  Step 1 — Loading raw data ...")
    raw_chunks = load_raw_text(data_path)
    print(f"  ✅  Raw chunks loaded: {len(raw_chunks)} profile blocks found")

    # ── Step 2: Parse ──
    print("\n  🔍  Step 2 — Parsing raw text into structured data ...")
    parsed = [parse_chunk(c) for c in raw_chunks]
    failed = sum(1 for p in parsed if p is None)
    print(f"  ✅  Parsed: {len(parsed) - failed} success | {failed} failed/skipped")

    # ── Step 3: Clean ──
    print("\n  🧹  Step 3 — Cleaning data ...")
    profiles = clean_profiles(parsed)
    print(f"  ✅  Clean profiles ready: {len(profiles)}")

    # ── Step 4: Save to JSON ──
    output_path = os.path.join("data", "parsed_profiles.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(profiles, f, indent=4, ensure_ascii=False)
    print(f"\n  💾  Structured data saved → {output_path}")

    # ── Step 5: Insights ──
    print("\n" + "─" * 60)
    print("  📊  Step 4 — Extracting Meaningful Insights")
    print("─" * 60)

    mp = get_max_posts(profiles)
    mf = get_max_followers(profiles)
    mfg = get_max_following(profiles)
    cats = get_category_breakdown(profiles)

    print(f"\n  📸  Who has the MAXIMUM POSTS?")
    print(f"      → @{mp['username']} ({mp['name']})")
    print(f"        {mp['no_of_posts']:,} posts | Category: {mp['type_of_page']}")

    print(f"\n  👥  Who has the MAXIMUM FOLLOWERS?")
    print(f"      → @{mf['username']} ({mf['name']})")
    print(f"        {mf['no_of_followers']:,} followers | Category: {mf['type_of_page']}")

    print(f"\n  🔁  Who FOLLOWS the MAXIMUM PEOPLE?")
    print(f"      → @{mfg['username']} ({mfg['name']})")
    print(f"        {mfg['no_of_following']:,} following | Category: {mfg['type_of_page']}")

    print(f"\n  🏷️   CATEGORY BREAKDOWN  ({len(cats)} unique categories)")
    print(f"  {'Category':<32} Count")
    print(f"  {'─'*32} ─────")
    for cat, count in cats.items():
        bar = "█" * count
        print(f"  {cat:<32} {count:>3}  {bar}")


# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("\n" + "█" * 60)
    print("█" + " " * 58 + "█")
    print("█" + "   🔍  SOCIALSCOPE — SOCIAL DATA INSIGHTS".center(58) + "█")
    print("█" + "   Pure Python | Data Science Project".center(58) + "█")
    print("█" + " " * 58 + "█")
    print("█" * 60)

    run_part1()
    run_part2()

    print("\n\n" + "═" * 60)
    print("  ✅  All done! SocialScope ran successfully.")
    print("  📁  Check data/parsed_profiles.json for structured output.")
    print("═" * 60 + "\n")
