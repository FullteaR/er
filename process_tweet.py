import re
import sys

reply_to = re.compile("@[0-9a-zA-Z_]+ ")
url = re.compile("https?://[0-9a-zA-Z-._~?&=/]+")


def process(tweet):
    if tweet[:3] == "RT ":  # リツイート
        return None
    tweet = reply_to.sub("", tweet)
    tweet = url.sub("", tweet)
    return tweet


if __name__ == "__main__":
    corpus_file = sys.argv[1]
    with open(corpus_file, "r") as fp:
        corpus = fp.readlines()  # 今回は個人のツイート程度の文量を対象としているためメモリ管理を気にしていませんが、扱うデータによってはメモリが耐えないかもしれません。
        corpus = [process(tweet) for tweet in corpus if process(tweet)]
    with open(corpus_file, "w") as fp:
        fp.writelines(corpus)
