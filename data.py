import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(42)

# Generate 100 rows of data
n_rows = 100

# Create date range for the last 3 months
end_date = datetime(2024, 1, 6)
start_date = end_date - timedelta(days=90)
dates = pd.date_range(start=start_date, end=end_date, periods=n_rows)

# Define post types with their respective base engagement rates
post_types = ['carousel', 'reel', 'static']
type_weights = [0.4, 0.35, 0.25]

# Base metrics for each post type
base_metrics = {
    'carousel': {
        'likes': (80, 200),
        'shares': (20, 60),
        'comments': (15, 45),
        'views': (800, 2000)
    },
    'reel': {
        'likes': (100, 300),
        'shares': (30, 90),
        'comments': (25, 75),
        'views': (1000, 3000)
    },
    'static': {
        'likes': (50, 150),
        'shares': (10, 40),
        'comments': (5, 25),
        'views': (500, 1500)
    }
}

# Generate data as a list of dictionaries
social_media_data = []

for i in range(n_rows):
    post_type = np.random.choice(post_types, p=type_weights)
    base = base_metrics[post_type]
    
    # Generate engagement metrics
    likes = int(np.random.uniform(base['likes'][0], base['likes'][1]) * (1 + np.random.normal(0, 0.2)))
    shares = int(np.random.uniform(base['shares'][0], base['shares'][1]) * (1 + np.random.normal(0, 0.2)))
    comments = int(np.random.uniform(base['comments'][0], base['comments'][1]) * (1 + np.random.normal(0, 0.2)))
    views = int(np.random.uniform(base['views'][0], base['views'][1]) * (1 + np.random.normal(0, 0.2)))
    
    # Ensure no negative values
    likes = max(0, likes)
    shares = max(0, shares)
    comments = max(0, comments)
    views = max(0, views)
    
    # Calculate engagement rate
    engagement_rate = round((likes + shares*2 + comments*3) / views * 100, 2)
    
    post = {
        "post_id": f"POST_{i+1:03d}",
        "type": post_type,
        "created_at": dates[i].strftime("%Y-%m-%d"),
        "likes": likes,
        "shares": shares,
        "comments": comments,
        "views": views,
        "engagement_rate": engagement_rate
    }
    
    social_media_data.append(post)

# Convert to JSON format
json_data = {
    "social_media_engagement": {
        "metadata": {
            "total_posts": n_rows,
            "date_range": {
                "start": start_date.strftime("%Y-%m-%d"),
                "end": end_date.strftime("%Y-%m-%d")
            },
            "post_types": list(base_metrics.keys())
        },
        "posts": social_media_data
    }
}

# Save to JSON file
with open('social_media_engagement.json', 'w') as f:
    json.dump(json_data, f, indent=2)

# Print sample of the data
print("Sample of the JSON data (first 2 posts):")
print(json.dumps({"social_media_engagement": {
    "metadata": json_data["social_media_engagement"]["metadata"],
    "posts": json_data["social_media_engagement"]["posts"][:2]
}}, indent=2))