import MeCab
import random
import time
import copy
try:
    from tqdm import tqdm
except:
    def tqdm(iter):
        return iter


class Markov:
    def __init__(self):
        self.BOS = "<BOS>"
        self.EOS = "<EOS>"
        self.db = {self.BOS: {}}
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
        words = [self.BOS] + \
            self.mecab.parse(text).strip().split(" ") + [self.EOS]
        while len(words) > 0:
            dictionary = self.db
            for i, word in enumerate(words):
                if word in dictionary:
                    dictionary = dictionary[word]
                    continue
                else:
                    dictionary[word] = self._create_deep_dictionary(
                        words[i + 1::])
                    break
            words.pop(0)
        return

    def speak(self, n, start=None):
        if (start in self.db.keys()) == False:
            start = self.BOS
        keywords = [start]
        dictionary = self.db
        retval = []

        while len(keywords) < n:
            dictionary = dictionary[keywords[-1]]
            try:
                next = random.choice(list(dictionary.keys()))
            except IndexError:  # nextが存在しない
                keywords = [self.BOS]
                dictionary = self.db
                continue
            next = str(next)
            keywords.append(next)
        retval = copy.copy(keywords)
        while keywords[-1] != self.EOS:
            dictionary = self.db
            for keyword in keywords:
                dictionary = dictionary[keyword]
            next = random.choice(list(dictionary.keys()))
            keywords.pop(0)
            keywords.append(next)
            retval.append(next)
        return "".join(retval)


if __name__ == "__main__":

    er = Markov()

    with open("./data/corpus.txt", "r") as fd:
        txt = fd.readlines()
        txt = [t.strip() for t in txt]
        for t in tqdm(txt):
            er.learn(t)

    while True:
        text=input()
        m=MeCab.Tagger(
            "-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd/")
        #words=[er.BOS]
        words=[]
        for l in m.parse(text).split("\n"):
            if ("\t" in l)==False:
                continue
            if l.split("\t")[1].split(",")[0]==("名詞" or "形容詞" or "形容動詞"):
                words.append(l.split("\t")[0])
        if words==[]:
            words=[er.BOS]
        print(er.speak(2,random.choice(words)))
