import tweepy, requests, os

USERNAME = 'WildVistas'
BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

client = tweepy.Client(bearer_token=BEARER_TOKEN)
user = client.get_user(username=USERNAME).data
tweets = client.get_users_tweets(id=user.id, max_results=5)

if not tweets.data:
    exit()

latest = tweets.data[0]
tweet_id = str(latest.id)

try:
    with open("last_tweet.txt", 'r') as f:
        last_id = f.read().strip()
except FileNotFoundError:
    last_id = None

if tweet_id != last_id:
    tweet_url = f"https://twitter.com/{USERNAME}/status/{tweet_id}"
    requests.post(WEBHOOK_URL, json={"content": f"{tweet_url}"})

    with open("last_tweet.txt","w") as f:
        f.write(tweet_id)
else:
    pass 
