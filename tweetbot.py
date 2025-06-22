import tweepy
import requests
import os

# Get credentials from GitHub Actions secrets
BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
USER_ID = os.getenv("TWITTER_USER_ID")

# Create Tweepy client
client = tweepy.Client(bearer_token=BEARER_TOKEN)

# Get the latest tweet from the user
import time
import tweepy.errors

MAX_RETRIES = 3
retry_delay = 60  # seconds
retry_count = 0

while retry_count < MAX_RETRIES:
    try:
        tweets = client.get_users_tweets(id=USER_ID, max_results=5)
        break  # Success — exit retry loop
    except tweepy.errors.TooManyRequests:
        retry_count += 1
        print(f"Rate limit hit. Retry {retry_count}/{MAX_RETRIES} in {retry_delay} seconds...")
        time.sleep(retry_delay)
else:
    print("Exceeded max retries due to rate limiting. Exiting.")
    exit(1)

latest = tweets.data[0]
tweet_id = str(latest.id)

# Check last posted tweet ID from file
try:
    with open("last_tweet.txt", "r") as f:
        last_id = f.read().strip()
except FileNotFoundError:
    last_id = "0"

# Post to Discord if it's a new tweet
if tweet_id != last_id:
    tweet_url = f"https://twitter.com/i/web/status/{tweet_id}"
    data = {"content": f"🕊️ New tweet:\n{tweet_url}"}
    response = requests.post(WEBHOOK_URL, json=data)

    if response.status_code == 204:
        print("Tweet posted to Discord.")
        with open("last_tweet.txt", "w") as f:
            f.write(tweet_id)
    else:
        print(f"Discord error: {response.status_code}")
else:
    print("No new tweet.")
