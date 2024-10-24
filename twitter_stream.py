import tweepy
from textblob import TextBlob
import pandas as pd

BEARER_TOKEN = 'add_token'

class MyStreamListener(tweepy.StreamingClient):
    def __init__(self, bearer_token):
        super().__init__(bearer_token)
        self.tweet_data = []

    def on_tweet(self, tweet):
        print(f"Tweet: {tweet.text}")

        analysis = TextBlob(tweet.text)
        polarity = analysis.sentiment.polarity
        subjectivity = analysis.sentiment.subjectivity

        print(f"Sentiment Polarity: {polarity}")
        print(f"Sentiment Subjectivity: {subjectivity}")
        print('---')

        self.tweet_data.append([tweet.text, polarity, subjectivity])

    def on_error(self, status_code):
        if status_code == 420:
            return False
        print(f"Error: {status_code}")

    def save_to_csv(self, file_name="LOTR_sentiment.csv"):
        df = pd.DataFrame(self.tweet_data, columns=['Tweet', 'Polarity', 'Subjectivity'])
        df.to_csv(file_name, index=False)
        print(f"Data saved to {file_name}")

stream_listener = MyStreamListener(BEARER_TOKEN)

stream_listener.add_rules(tweepy.StreamRule("LOTR"))
stream_listener.add_rules(tweepy.StreamRule("Lord of the Rings"))
stream_listener.add_rules(tweepy.StreamRule("#LOTR"))
stream_listener.add_rules(tweepy.StreamRule("The Rings of Power"))

try:
    stream_listener.filter(tweet_fields=["text"])
except KeyboardInterrupt:
    stream_listener.save_to_csv()