import os
import requests
import re
import sys
from datetime import datetime, timedelta, timezone

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
OUTPUT_FOLDER = "./downloads"
OUTPUT_FILE = "hn_it_news.txt"
OUTPUT_FILE_PATH = OUTPUT_FOLDER + "/" + OUTPUT_FILE
TIMEZONE_OFFSET = 7  # GMT+7

bar_length = 30


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
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    now = datetime.now()
    datetime_str = now.strftime("%Y%m%d_%H%M%S")
    file_name_using_datetime = OUTPUT_FILE.replace(".txt", f"_{datetime_str}.txt")
    output_file_path = OUTPUT_FOLDER + "/" + file_name_using_datetime

    # if os.path.exists(OUTPUT_FILE_PATH):
    #     os.remove(OUTPUT_FILE_PATH)
    #     print(f"✅ Deleted the old {OUTPUT_FILE_PATH}")
    # else:
    #     print(f"⚠ {OUTPUT_FILE_PATH} does not exist")

    print("\n🔍 Getting Hacker News...")

    story_ids = get_story_ids("top")[:MAX_STORIES] + get_story_ids("new")[:MAX_STORIES]
    length = len(story_ids)
    results = []

    for i, sid in enumerate(story_ids, start=1):
        story = get_story_detail(sid)
        if story and "title" in story and matches_keywords(story["title"]):
            story_time = datetime.fromtimestamp(
                story.get("time", 0), timezone.utc
            ) + timedelta(hours=TIMEZONE_OFFSET)
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
        percent = int(i / length * 100)
        filled = int(bar_length * i / length)
        bar = "█" * filled + "-" * (bar_length - filled)
        sys.stdout.write(f"\r|{bar}| {percent}% ({i}/{length})")
        sys.stdout.flush()

    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write(
            f"Hacker News IT Stories (Top + New) - {datetime.now() + timedelta(hours=TIMEZONE_OFFSET)} GMT+7\n\n"
        )
        for r in results:
            f.write(f"{r['time']} | {r['title']} (Score: {r['score']})\n{r['url']}\n\n")

    print(f"\n\n✅ Saved {len(results)} at {output_file_path}")


if __name__ == "__main__":
    main()
