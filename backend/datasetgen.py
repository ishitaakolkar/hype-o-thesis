import praw
import pandas as pd
import time
import os
from datetime import datetime

# ==== Reddit API Setup ====
reddit = praw.Reddit(
    client_id='YOUR_CLIENT_ID',
    client_secret='YOUR_CLIENT_SECRET',
    user_agent='trend-predictor'
)

# ==== Config ====
SUBREDDIT = 'technology'   # Change as needed
CSV_FILE = 'rising_posts.csv'
FETCH_LIMIT = 25
INTERVAL = 300  # 5 minutes

# ==== Load or Create Dataset ====
if os.path.exists(CSV_FILE):
    df = pd.read_csv(CSV_FILE)
else:
    df = pd.DataFrame(columns=[
        'post_id', 'title', 'created_utc', 'initial_score',
        'author', 'subreddit', 'flair', 'url', 
        'score_updates', 'comment_updates'
    ])

# Convert created_utc to datetime for time delta tracking
def time_since_post(created_utc):
    return (datetime.utcnow() - datetime.utcfromtimestamp(created_utc)).total_seconds() // 60

# ==== Main Loop ====
while True:
    print(f"\n[⏳] Fetching rising posts from r/{SUBREDDIT} at {datetime.utcnow()}")

    subreddit = reddit.subreddit(SUBREDDIT)
    rising_posts = subreddit.rising(limit=FETCH_LIMIT)

    for post in rising_posts:
        existing = df[df['post_id'] == post.id]

        if existing.empty:
            print(f"[🆕] Tracking new post: {post.title[:60]}")

            df = pd.concat([df, pd.DataFrame([{
                'post_id': post.id,
                'title': post.title,
                'created_utc': post.created_utc,
                'initial_score': post.score,
                'author': str(post.author),
                'subreddit': post.subreddit.display_name,
                'flair': post.link_flair_text,
                'url': post.url,
                'score_updates': str([post.score]),
                'comment_updates': str([post.num_comments])
            }])], ignore_index=True)
        else:
            idx = existing.index[0]

            score_list = eval(existing.iloc[0]['score_updates'])
            comment_list = eval(existing.iloc[0]['comment_updates'])

            score_list.append(post.score)
            comment_list.append(post.num_comments)

            df.at[idx, 'score_updates'] = str(score_list)
            df.at[idx, 'comment_updates'] = str(comment_list)

            print(f"[📈] Updated: {post.title[:40]} | Score: {post.score} | Comments: {post.num_comments}")

    # Save updated dataframe to CSV
    df.to_csv(CSV_FILE, index=False)
    print(f"[💾] Saved {len(df)} tracked posts to {CSV_FILE}")

    print(f"[⏳] Sleeping for {INTERVAL//60} minutes...\n")
    time.sleep(INTERVAL)