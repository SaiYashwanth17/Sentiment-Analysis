import re
import tweepy
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
from tweepy import OAuthHandler
from textblob import TextBlob
class TwitterClient(object):
    def __init__(self):
        # keys and tokens from the Twitter Dev Console
        consumer_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxx'
        consumer_secret = 'xxxxxxxxxxxxxxxxxxxxxxxxxx'
        access_token = 'xxxxxxxxxxxxxxxxxxxxxxxxxx'
        access_token_secret = 'xxxxxxxxxxxxxxxxxxxxxxxxxx'
        try:
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(self.auth)
        except:
            print("Authentication Failed")
    def clean_text(self, text):
        tokens = word_tokenize(text)
        tokens = [w.lower() for w in tokens]
        table = str.maketrans('', '', string.punctuation)
        stripped = [w.translate(table) for w in tokens]
        words = [word for word in stripped if word.isalpha()]
        stop_words = set(stopwords.words('english'))
        words = [w for w in words if not w in stop_words]
        txt = ' '.join([word for word in words])
        return txt
        # return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])| (\w+:/ \ / \ S+)", " ", text).split())
    def tweet_sentiment(self, tweet):
        analysis = TextBlob(self.clean_text(tweet))
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
    def get_tweets(self, query, count = 10):
        tweets = []
        try:
            fetched_tweets = self.api.search(q=query, count=count)
            for tweet in fetched_tweets:
                parsed_tweet = {}
                parsed_tweet['text'] = tweet.text
                parsed_tweet['sentiment'] = self.tweet_sentiment(tweet.text)
                if tweet.retweet_count > 0:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
            return tweets
        except tweepy.TweepError as e:
            print("Error : " + str(e))


def main():
    api = TwitterClient()
    tweets = api.get_tweets(query='bill gates', count=200)

    # picking positive tweets
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    # percentage of positive tweets
    print("Positive tweets percentage: {} %".format(100 * len(ptweets) / len(tweets)))
    # picking negative tweets
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    # percentage of negative tweets
    print("Negative tweets percentage: {} %".format(100 * len(ntweets) / len(tweets)))
    # percentage of neutral tweets
    print("Neutral tweets percentage: {} % \
          ".format(100 * (len(tweets) - (len(ntweets) + len(ptweets))) / len(tweets)))

    ## printing first 5 positive tweets
    print("\n\nPositive tweets:")
    for tweet in ptweets[:5]:
        print(tweet['text'])

    ## printing first 5 negative tweets
    print("\n\nNegative tweets:")
    for tweet in ntweets[:5]:
        print(tweet['text'])

if __name__ == "__main__":
    # calling main function
    main()