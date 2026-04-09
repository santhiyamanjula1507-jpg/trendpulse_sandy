import requests
import json
import time
import os
from datetime import datetime

print("🚀 Script started...")

# -------------------------------
# API URLs
# -------------------------------
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

headers = {"User-Agent": "TrendPulse/1.0"}

# -------------------------------
# Category keywords
# -------------------------------
categories = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

# -------------------------------
# Category function
# -------------------------------
def get_category(title):
    if not title:
        return "other"

    title = title.lower()

    for category, keywords in categories.items():
        for word in keywords:
            if word in title:
                return category

    return "other"   # IMPORTANT FIX

# -------------------------------
# Fetch top stories
# -------------------------------
try:
    print("📡 Fetching top stories...")
    response = requests.get(TOP_STORIES_URL, headers=headers)
    story_ids = response.json()[:500]
    print("✅ Fetched IDs:", len(story_ids))
except Exception as e:
    print("❌ Error fetching top stories:", e)
    story_ids = []

# -------------------------------
# Fetch story details
# -------------------------------
collected_data = []
category_count = {cat: 0 for cat in categories}
category_count["other"] = 0   # track extra

for story_id in story_ids:
    try:
        res = requests.get(ITEM_URL.format(story_id), headers=headers)
        story = res.json()

        if not story or "title" not in story:
            continue

        print("Processing:", story_id)   # DEBUG PRINT

        category = get_category(story["title"])

        # Limit 25 per main categories
        if category in categories and category_count[category] >= 25:
            continue

        data = {
            "post_id": story.get("id"),
            "title": story.get("title"),
            "category": category,
            "score": story.get("score", 0),
            "num_comments": story.get("descendants", 0),
            "author": story.get("by"),
            "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        collected_data.append(data)

        if category in category_count:
            category_count[category] += 1

        # Stop when enough data collected
        if len(collected_data) >= 120:
            break

    except Exception as e:
        print(f"⚠️ Error with story {story_id}: {e}")
        continue

# -------------------------------
# Save file
# -------------------------------
if not os.path.exists("data"):
    os.makedirs("data")

filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

with open(filename, "w", encoding="utf-8") as f:
    json.dump(collected_data, f, indent=4)

# -------------------------------
# Final output
# -------------------------------
print("\n🎯 DONE")
print("Total collected:", len(collected_data))
print(f"Saved to: {filename}")



