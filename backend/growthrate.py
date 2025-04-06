import pandas as pd
import ast

df = pd.read_csv("rising_posts.csv")

def extract_features(row):
    scores = ast.literal_eval(row['score_updates'])
    comments = ast.literal_eval(row['comment_updates'])

    features = {}
    if len(scores) >= 4:
        features['score_t0'] = scores[0]
        features['score_t3'] = scores[3]
        features['growth_0_3'] = scores[3] - scores[0]
        features['avg_growth_rate'] = (scores[3] - scores[0]) / 15

        # Acceleration: (change between t1-t2) - (t0-t1)
        delta1 = scores[1] - scores[0]
        delta2 = scores[2] - scores[1]
        features['score_acceleration'] = delta2 - delta1
    else:
        # Fill with -1 or default if not enough data
        features['score_t0'] = -1
        features['score_t3'] = -1
        features['growth_0_3'] = -1
        features['avg_growth_rate'] = -1
        features['score_acceleration'] = -1

    if len(comments) >= 4:
        features['comment_growth'] = (comments[3] - comments[0]) / 15
    else:
        features['comment_growth'] = -1

    return pd.Series(features)

# Apply to each row
features_df = df.apply(extract_features, axis=1)

# Combine with the original
final_df = pd.concat([df, features_df], axis=1)
final_df.to_csv("features_dataset.csv", index=False)
print("✅ Features extracted and saved!")