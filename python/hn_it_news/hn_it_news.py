import os
import requests
import re
from datetime import datetime, timedelta

KEYWORDS = [
    "python",
    "javascript",
    "programming",
    "developer",
    "software",
    "AI",
    "cloud",
    "database",
    "linux",
    "reactjs",
    "nextjs",
    "nodejs",
    "nestjs",
]
MAX_STORIES = 50
OUTPUT_FILE = "hn_it_news.txt"
TIMEZONE_OFFSET = 7  # GMT+7


def get_story_ids(story_type="top"):
    url = f"https://hacker-news.firebaseio.com/v0/{story_type}stories.json"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()


def get_story_detail(story_id):
    url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()


def matches_keywords(title):
    title_lower = title.lower()
    return any(re.search(rf"\b{kw.lower()}\b", title_lower) for kw in KEYWORDS)


def main():
    if os.path.exists("hn_it_news.txt"):
        os.remove("hn_it_news.txt")
        print("✅ Deleted hn_it_news.txt")
    else:
        print("⚠ hn_it_news.txt does not exist")
    print("🔍 Getting Hacker News...")

    story_ids = get_story_ids("top")[:MAX_STORIES] + get_story_ids("new")[:MAX_STORIES]
    results = []

    for sid in story_ids:
        print(sid)
        story = get_story_detail(sid)
        if story and "title" in story and matches_keywords(story["title"]):
            story_time = datetime.utcfromtimestamp(story.get("time", 0)) + timedelta(
                hours=TIMEZONE_OFFSET
            )
            results.append(
                {
                    "title": story["title"],
                    "url": story.get(
                        "url", f"https://news.ycombinator.com/item?id={sid}"
                    ),
                    "score": story.get("score", 0),
                    "time": story_time.strftime("%Y-%m-%d %H:%M:%S"),
                }
            )

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(
            f"Hacker News IT Stories (Top + New) - {datetime.utcnow() + timedelta(hours=TIMEZONE_OFFSET)} GMT+7\n\n"
        )
        for r in results:
            f.write(f"{r['time']} | {r['title']} (Score: {r['score']})\n{r['url']}\n\n")

    print(f"✅ Saved {len(results)} at {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
