from collect_tweet import getAllTweet, api
import tweepy
import sys
import time


def getAllReply(id):
    for tweet in getAllTweet(id):
        with open("./data/talk.txt", "a") as fp:
            if tweet._json.get("in_reply_to_status_id", None) != None:
                #print(tweet.text)
                try:
                    fp.write(
                        "???\t" + api.get_status(int(tweet._json["in_reply_to_status_id"])).text.replace("\n", ""))
                    fp.write("\n")
                    fp.write("塚田 恵理\t" + tweet.text.replace("\n", ""))
                    fp.write("\n")
                except tweepy.error.RateLimitError:
                    time.sleep(60*15)
                except tweepy.error.TweepError:
                    pass


if __name__ == "__main__":
    for account in sys.argv[1::]:
        getAllReply(account)
