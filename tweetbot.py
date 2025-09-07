import tweepy
import requests
import os
import time
import tweepy.errors

# --- Configuration ---
BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
USER_ID = os.getenv("TWITTER_USER_ID")

# --- Tweepy Client ---
client = tweepy.Client(bearer_token=BEARER_TOKEN)

# --- Read last seen tweet ID ---
try:
    with open("last_tweet.txt", "r") as f:
        last_id = int(f.read().strip())
except (FileNotFoundError, ValueError):
    last_id = 0

# --- Retry logic for rate limits ---
MAX_RETRIES = 1
retry_delay = 30
retry_count = 0

while retry_count < MAX_RETRIES:
    try:
        tweets = client.get_users_tweets(
            id=USER_ID,
            max_results=10,
            since_id=last_id if last_id > 0 else None
        )
        break
    except tweepy.errors.TooManyRequests:
        retry_count += 1
        print(f"Rate limit hit. Retry {retry_count}/{MAX_RETRIES} in {retry_delay} seconds...")
        time.sleep(retry_delay)
else:
    print("Exceeded max retries. Exiting.")
    exit(1)

# --- Filter new tweets ---
new_tweets = [t for t in tweets.data if int(t.id) > last_id] if tweets.data else []
new_tweets.sort(key=lambda x: int(x.id))  # oldest to newest

# --- Post each new tweet to Discord ---
for tweet in new_tweets:
    tweet_url = f"https://twitter.com/i/web/status/{tweet.id}"
    data = {"content": f"{tweet_url}"}
    response = requests.post(WEBHOOK_URL, json=data)

    if response.status_code == 204:
        print(f"✅ Posted tweet {tweet.id} to Discord.")
        last_id = max(last_id, int(tweet.id))
    else:
        print(f"❌ Failed to post tweet {tweet.id}: HTTP {response.status_code}")

# --- Update last_tweet.txt ---
if new_tweets:
    with open("last_tweet.txt", "w") as f:
        f.write(str(last_id))
else:
    print("No new tweets to post.")


