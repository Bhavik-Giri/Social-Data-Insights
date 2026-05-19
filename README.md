# 🔍 SocialScope — Social Media Data Insights

> **A pure Python data science project** that combines a social network recommendation engine with real Instagram follower analytics — built from scratch without pandas, NumPy, or any data science libraries.

<br>

## 📌 Project Overview

This project was built as part of a **Data Science internship simulation** to demonstrate the complete data science pipeline:

```
Raw Data  →  Parsing  →  Cleaning  →  Structuring  →  Insights
```

It has **two independent parts** that run together from a single `main.py`:

| Part | What It Does |
|------|--------------|
| **Part 1** — CodeBook Recommendation Engine | Loads JSON social graph data, cleans it, then runs two recommendation algorithms: *People You May Know* and *Pages You Might Like* |
| **Part 2** — Coders of Bangalore Analytics | Collects raw Instagram profile text, parses it into structured data, cleans it, and extracts 4 meaningful insights |

<br>

---

## 🗂️ Project Structure

```
Social-Data-Insights/
│
├── main.py                          ← Entry point — runs everything
│
├── data/
│   ├── massive_data.json            ← CodeBook social graph (30 users, 27 pages)
│   ├── finaldata.txt                ← Raw Instagram profiles (107 accounts)
│   ├── initialdata.txt              ← Sample/test data (13 accounts)
│   └── parsed_profiles.json         ← Auto-generated after running main.py
│
├── part1_recommendations/
│   ├── __init__.py
│   ├── load_data.py                 ← JSON file loader
│   ├── data_cleaning.py             ← Data cleaning logic
│   ├── people_you_may_know.py       ← Mutual-friend recommendation algorithm
│   └── pages_you_might_like.py      ← Shared-interest page recommendation
│
├── part2_openai_analytics/
│   ├── __init__.py
│   ├── data_collector.py            ← Raw data loading + chunking
│   ├── data_parser.py               ← Text parser (handles K/M suffixes)
│   ├── data_cleaner.py              ← Dedup + validation
│   └── insights.py                  ← 4 analytics functions
│
├── .gitignore
├── requirements.txt
└── README.md
```

<br>

---

## 🧠 Part 1 — Social-media Recommendation Engine

### Dataset
A JSON social graph of **30 users** and **27 pages** (CodeBook — a fictional social platform for coders). Each user has a list of friends (by ID) and liked pages (by ID).

### Feature 1: People You May Know

**Logic:** If User A and User B are not directly friends but share mutual friends, suggest B to A. More mutual friends = higher rank in suggestions.

```
Algorithm:
  For each direct friend of User X:
    For each friend-of-friend (mutual):
      If mutual ≠ X and mutual ∉ X's direct friends:
        mutual_count += 1
  Sort by mutual_count descending → return ranked list
```

**Sample Output:**
```
@Amit (ID 1) — You may know:
  1. Kunal       ← 2 mutual friends
  2. Anjali      ← 2 mutual friends
  3. Ravi        ← 1 mutual friend
  4. Sneha       ← 1 mutual friend
  5. Arjun       ← 1 mutual friend
```

### Feature 2: Pages You Might Like

**Logic:** Find users who liked at least one of the same pages as you. Then recommend pages they liked that you haven't seen yet. More shared pages with the recommender = higher score.

```
Algorithm:
  For each other user:
    shared_pages = intersection(your_pages, their_pages)
    if shared_pages is not empty:
      For each page they liked that you haven't:
        page_score += len(shared_pages)
  Sort by score descending → return top N
```

**Sample Output:**
```
@Amit (ID 1) — Recommended pages:
  1. AI & ML Community       (score: 2)
  2. Blockchain Innovators   (score: 1)
  3. Cloud Computing Pros    (score: 1)
```

### Data Cleaning Applied
Before running recommendations, the raw data is cleaned:

| Issue | Fix Applied |
|-------|-------------|
| Empty/missing username | Removed |
| Duplicate friend entries | `list(set(friends))` |
| Inactive users (no friends, no liked pages) | Removed |
| Duplicate page IDs | Keep last entry using dict keying |

<br>

---

## 📊 Part 2 — Instagram Analytics

### Dataset
**107 raw Instagram profiles** manually collected from the Bangalore tech community (OpenAI followers). Data stored as plain text — one profile block per entry, separated by blank lines.

### Raw Data Format
```
startuphub_blr
2,300 posts
45K followers
120 following
Startup Hub Bangalore
Media
🦄 News from the Silicon Valley of India
📢 Funding alerts, Hiring trends, and Drama
```

### The Pipeline

```
Step 1 — LOAD       finaldata.txt  →  107 raw text chunks
Step 2 — PARSE      text chunks    →  Python dictionaries (handles K/M)
Step 3 — CLEAN      raw dicts      →  105 valid unique profiles
Step 4 — INSIGHTS   clean data     →  4 answers + category chart
```

### Parser Logic
The parser handles real-world messy data:
- `45K followers` → `45,000`
- `681K followers` → `681,000`
- `1.2M followers` → `1,200,000`
- Missing category → defaults to `"Unknown"`
- Malformed block → returns `None`, silently skipped

### 📈 Insights — Real Results

**1. Who has the maximum posts?**
```
→ @startuphub_blr  (Startup Hub Bangalore)
  2,300 posts | Category: Media
```

**2. Who has the maximum followers?**
```
→ @_anujsinghal  (Anuj Singhal)
  681,000 followers | Category: Digital creator
  Managing Editor, CNBC-Awaaz
```

**3. Who follows the maximum people?**
```
→ @bangalore_tech_bro  (Rahul | HSR Hustler)
  890 following | Category: Entrepreneur
```

**4. How many categories exist?**
```
34 unique categories across 105 profiles

Top categories:
  Community           →  33 accounts  ████████████████████████████████
  Media               →  11 accounts  ███████████
  Blog                →   8 accounts  ████████
  Tech                →   6 accounts  ██████
  Personal Blog       →   5 accounts  █████
  Education           →   4 accounts  ████
  ... and 28 more
```

<br>

---

## 🚀 How to Run

### Step 1 — Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/SocialScope.git
cd SocialScope
```

### Step 2 — No installation needed!
This project uses **only Python's standard library** — no `pip install` required.

Verify you have Python 3:
```bash
python --version
# or
python3 --version
```

### Step 3 — Make sure your data files are in place
```
SocialScope/
└── data/
    ├── massive_data.json    ✅ required for Part 1
    └── finaldata.txt        ✅ required for Part 2
```

### Step 4 — Run the project
```bash
python main.py
# or on some systems:
python3 main.py
```

### Step 5 — Expected output
You will see:
- Part 1: People You May Know + Pages You Might Like for 3 sample users
- Part 2: Full pipeline steps + all 4 insights with a category bar chart
- A new file `data/parsed_profiles.json` will be auto-created

<br>

---

## 🛠️ Tech Stack

| Item | Detail |
|------|--------|
| Language | Python 3.x |
| Libraries | `json`, `os` (standard library only) |
| Data formats | `.json`, `.txt` |
| External dependencies | **None** |

<br>

---

## 💡 Key Concepts Demonstrated

| Concept | Where Used |
|---------|-----------|
| JSON loading & dumping | Part 1 — CodeBook data |
| String parsing & cleaning | Part 2 — raw Instagram text |
| Set operations (intersection) | Pages You Might Like algorithm |
| Dictionary as a frequency counter | Mutual friends count, category count |
| Sorting with `key=lambda` | All ranking/recommendation outputs |
| List comprehensions | Data cleaning throughout |
| Handling real-world messy data | K/M suffix parsing, missing fields |
| Modular code design | Split across logical files/modules |

<br>

---

## 📁 Output File

After running `main.py`, a file `data/parsed_profiles.json` is automatically generated.
It contains all 105 clean profiles in structured JSON format:

```json
[
    {
        "username": "startuphub_blr",
        "no_of_posts": 2300,
        "no_of_followers": 45000,
        "no_of_following": 120,
        "name": "Startup Hub Bangalore",
        "type_of_page": "Media",
        "bio": "..."
    },
    ...
]
```

<br>

---

## 👨‍💻 Author

**Your Name**
Aspiring Data Scientist | Pure Python Enthusiast

- 🔗 [LinkedIn](https://linkedin.com/in/YOUR_PROFILE)
- 🐙 [GitHub](https://github.com/YOUR_USERNAME)

<br>

---

## 🎯 Purpose

This project was built as part of a **Data Science course** to practice:
- Real-world data collection and parsing
- Building algorithms from scratch (no ML libraries)
- Writing clean, modular, production-ready Python
- Extracting and presenting meaningful insights from raw data

> *"The best way to learn data science is to do data science."*
