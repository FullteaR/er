from markov import Markov
from talk_module import talk
try:
    from tqdm import tqdm
except:
    def tqdm(iter):
        return iter
import random
import MeCab

if __name__ == "__main__":
    er = Markov()

    with open("./data/corpus.txt", "r") as fd:
        txt = fd.readlines()
        txt = [t.strip() for t in txt]
        for t in tqdm(txt):
            er.learn(t)

    m = MeCab.Tagger(
        "-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd/")
    while True:
        text = talk(input(">"))
        words = []

        for l in m.parse(text).split("\n"):
            if ("\t" in l) == False:
                continue
            if l.split("\t")[1].split(",")[0] in ("名詞", "形容詞", "形容動詞", "副詞", "感動詞"):
                words.append(l.split("\t")[0])
        if words == []:
            words = [er.BOS]
        reply = er.speak(2, random.choice(words))
        reply = reply.replace(er.BOS, "")
        reply = reply.replace(er.EOS, "")
        print(reply)
