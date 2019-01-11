import tweepy
from keys import consumerKey, consumerSecret, myAccessToken, myAccessTokenSecret
import sys

auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(myAccessToken, myAccessTokenSecret)
api = tweepy.API(auth)


def getAllTweet(id):
    i = 0
    while True:
        tweets = api.user_timeline(id=id, page=i)
        for tweet in tweets:
            yield tweet
        if len(tweets) == 0:
            return
        i += 1


def writeAllTweet(fp, id):
    for tweet in getAllTweet(id):
        fp.write(tweet.text)
        print(tweet.text)
        fp.write("\n")


if __name__ == "__main__":
    ids = sys.argv[1::]
    with open("./data/corpus.txt", "a") as fp:
        for id in ids:
            writeAllTweet(fp, id)
