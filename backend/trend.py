import praw
import time

# ==== Reddit API Setup ====
reddit = praw.Reddit(
    client_id='YOUR_CLIENT_ID',
    client_secret='YOUR_CLIENT_SECRET',
    user_agent='trend-predictor-app'
)

# === Config ===
subreddit_name = 'technology'  # change to any subreddit
track_interval = 300  # in seconds (e.g., every 5 minutes)
top_n = 5  # How high in 'hot' to count as "trending"

# === Data structure to track rising posts ===
tracked_posts = {}

def fetch_rising_posts():
    rising_posts = reddit.subreddit(subreddit_name).rising(limit=25)
    for post in rising_posts:
        if post.id not in tracked_posts:
            tracked_posts[post.id] = {
                'title': post.title,
                'created': post.created_utc,
                'initial_upvotes': post.score,
                'in_hot_top': False
            }

def check_hot_list():
    hot_posts = list(reddit.subreddit(subreddit_name).hot(limit=top_n))
    hot_ids = {post.id for post in hot_posts}

    for post_id, info in tracked_posts.items():
        if not info['in_hot_top'] and post_id in hot_ids:
            info['in_hot_top'] = True
            print(f"[🔥 TRENDING] '{info['title']}' made it to top {top_n} hot!")

def print_tracked():
    print("\n--- Tracked Rising Posts ---")
    for pid, info in tracked_posts.items():
        print(f"{'[HOT]' if info['in_hot_top'] else '[   ]'} {info['title']}")

# === Main Loop ===
try:
    while True:
        print("\n[⏳] Checking rising posts...")
        fetch_rising_posts()
        check_hot_list()
        print_tracked()
        time.sleep(track_interval)  # Wait before next check

except KeyboardInterrupt:
    print("\n[💾] Exiting and saving data...")