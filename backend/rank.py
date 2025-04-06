import pandas as pd
import praw

# ==== Reddit API ====
reddit = praw.Reddit(
    client_id='YOUR_CLIENT_ID',
    client_secret='YOUR_CLIENT_SECRET',
    user_agent='trend-predictor'
)

# ==== Load Rising Post Data ====
df = pd.read_csv('rising_posts.csv')
df['final_rank'] = None  # Add column if not there

# ==== Get Top Posts of the Week ====
subreddit_name = 'technology'
top_posts = list(reddit.subreddit(subreddit_name).top(time_filter='week', limit=100))
top_ids = [post.id for post in top_posts]

# ==== Assign Ranks ====
for i, post_id in enumerate(top_ids):
    if post_id in df['post_id'].values:
        df.loc[df['post_id'] == post_id, 'final_rank'] = i + 1  # Rank is 1-based

# ==== Fill missing with 100 (optional) ====
df['final_rank'] = df['final_rank'].fillna(100).astype(int)

# ==== Save Labeled Dataset ====
df.to_csv('labeled_posts.csv', index=False)
print("✅ Final ranks assigned and saved to labeled_posts.csv")