import MeCab
import random
import time
import copy
from tqdm import tqdm


class Markov:
    def __init__(self):
        self.BOS = "<BOS>"
        self.EOS = "<EOS>"
        self.db = {self.BOS:{}}
        self.mecab = MeCab.Tagger(
            "-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd/ -Owakati")

    def _create_deep_dictionary(self, list_):
        """
        list=[a,b,c,d,e]を{a:{b:{c:{d:{e}}}}}に変換する。
        """
        if len(list_) == 0:
            return {}
        elif len(list_) == 0:
            return {list_[0]}
        else:
            retval = {}
            retval[list_[0]] = self._create_deep_dictionary(list_[1::])
            return retval

    def learn(self, text):
        if text == "":
            return
        words = [self.BOS] + self.mecab.parse(text).strip().split(" ") + [self.EOS]
        while len(words) > 0:
            dictionary=self.db
            for i,word in enumerate(words):
                if word in dictionary:
                    dictionary=dictionary[word]
                    continue
                else:
                    dictionary[word]=self._create_deep_dictionary(words[i+1::])
                    break
            words.pop(0)
        return

    def speak(self, n):
        keywords=[self.BOS]
        dictionary=self.db
        retval=""

        while len(keywords)<n:
            dictionary=dictionary[keywords[-1]]
            try:
                next=random.choice(list(dictionary.keys()))
            except IndexError:#nextが存在しない
                keywords=[self.BOS]
                dictionary=self.db
                continue
            next=str(next)
            keywords.append(next)
        retval="".join(keywords)
        while keywords[-1]!=self.EOS:
            dictionary=self.db
            for keyword in keywords:
                dictionary=dictionary[keyword]
            next=random.choice(list(dictionary.keys()))
            keywords.pop(0)
            keywords.append(next)
            retval+=next
        return retval


if __name__ == "__main__":

    er = Markov()

    with open("./data/corpus.txt", "r") as fd:
        txt = fd.readlines()
        txt = [t.strip() for t in txt]
        for t in tqdm(txt):
            er.learn(t)

    for i in range(10):
        print(er.speak(2))
    for i in range(10):
        print(er.speak(5))
